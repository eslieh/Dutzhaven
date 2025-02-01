import unittest
import json
from flask import create_app
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class UserTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed_password = generate_password_hash('testpassword', method='sha256')
            self.test_user = User(username='testuser', email='test@example.com', password_hash=hashed_password, user_type='client')
            db.session.add(self.test_user)
            db.session.commit()
            self.token = create_access_token(identity=self.test_user.id)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_get_profile(self):
        response = self.client.get('/users/profile', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['username'], 'testuser')
        self.assertEqual(response_data['email'], 'test@example.com')
        self.assertEqual(response_data['user_type'], 'client')

    def test_get_user(self):
        hashed_password = generate_password_hash('anotherpassword', method='sha256')
        another_user = User(username='anotheruser', email='another@example.com', password_hash=hashed_password, user_type='freelancer')
        with self.app.app_context():
            db.session.add(another_user)
            db.session.commit()

        response = self.client.get(f'/users/{another_user.id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['username'], 'anotheruser')
        self.assertEqual(response_data['user_type'], 'freelancer')
        self.assertEqual(response_data['email'], 'another@example.com')

    def test_update_profile(self):
        updated_data = {'bio': 'Updated bio', 'contact_info': 'Updated contact info'}
        response = self.client.put('/users/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Profile updated successfully')

        with self.app.app_context():
            user = User.query.get(self.test_user.id)
            self.assertEqual(user.bio, 'Updated bio')
            self.assertEqual(user.contact_info, 'Updated contact info')

    def test_update_profile_missing_data(self):
        updated_data = {'bio': 'Updated bio'}
        response = self.client.put('/users/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            user = User.query.get(self.test_user.id)
            self.assertEqual(user.bio, 'Updated bio')
            self.assertEqual(user.contact_info, self.test_user.contact_info)

    def test_update_profile_unauthorized(self):
        hashed_password = generate_password_hash('anotherpassword', method='sha256')
        another_user = User(username='anotheruser', email='another@example.com', password_hash=hashed_password, user_type='freelancer')
        with self.app.app_context():
            db.session.add(another_user)
            db.session.commit()

        updated_data = {'bio': 'Trying to update another user bio'}
        response = self.client.put(f'/users/{another_user.id}/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 403)

        with self.app.app_context():
            retrieved_user = User.query.get(another_user.id)
            self.assertNotEqual(retrieved_user.bio, 'Trying to update another user bio')

    def test_update_profile_invalid_data(self):
        updated_data = {'email': 'invalid-email'}
        response = self.client.put('/users/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn("Invalid", response_data['message'])

    def test_get_profile_not_found(self):
        invalid_token = create_access_token(identity=999)
        response = self.client.get('/users/profile', headers={'Authorization': f'Bearer {invalid_token}'})
        self.assertEqual(response.status_code, 404)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'User not found')