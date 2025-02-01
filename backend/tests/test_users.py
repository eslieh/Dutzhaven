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

    def test_update_profile(self):
        updated_data = {'bio': 'Updated bio', 'contact_info': 'Updated contact info'}
        response = self.client.put('/users/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Profile updated successfully')

        with self.app.app_context():  # Check if the profile is updated in the database
            user = User.query.get(self.test_user.id)
            self.assertEqual(user.bio, 'Updated bio')
            self.assertEqual(user.contact_info, 'Updated contact info')

    def test_update_profile_missing_data(self):
        # Test updating with only one field
        updated_data = {'bio': 'Updated bio'}
        response = self.client.put('/users/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            user = User.query.get(self.test_user.id)
            self.assertEqual(user.bio, 'Updated bio')  # Bio should be updated
            # Contact info should not be changed
            self.assertEqual(user.contact_info, self.test_user.contact_info)

    def test_update_profile_unauthorized(self):
        # Try to update another user's profile (should not be allowed)
        hashed_password = generate_password_hash('anotherpassword', method='sha256')
        another_user = User(username='anotheruser', email='another@example.com', password_hash=hashed_password, user_type='freelancer')
        with self.app.app_context():
            db.session.add(another_user)
            db.session.commit()

        updated_data = {'bio': 'Trying to update another user bio'}
        response = self.client.put(f'/users/{another_user.id}/profile', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 404) # Or 403 if you handle it differently

        with self.app.app_context(): # Ensure the other user's bio was not changed
            retrieved_user = User.query.get(another_user.id)
            self.assertNotEqual(retrieved_user.bio, 'Trying to update another user bio') # Or assertEqual to original value