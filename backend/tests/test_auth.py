import unittest
import json
from flask import create_app
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed_password = generate_password_hash('testpassword', method='sha256')
            self.test_user = User(username='testuser', email='test@example.com', password_hash=hashed_password, user_type='client')
            db.session.add(self.test_user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_register(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123',
            'user_type': 'freelancer'
        }
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'User registered successfully')
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['username'], 'newuser')

        with self.app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.email, 'new@example.com')
            self.assertEqual(user.user_type, 'freelancer')

    def test_register_duplicate_username(self):
        data = {
            'username': 'testuser',
            'email': 'diff@example.com',
            'password': 'password123',
            'user_type': 'client'
        }
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Username already exists')

    def test_register_missing_fields(self):
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'password123'
        }
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Missing required fields')

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['username'], 'testuser')

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Invalid credentials')

    def test_login_user_not_found(self):
        data = {
            'username': 'nonexistentuser',
            'password': 'password123'
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Invalid credentials')

    def test_check_token(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_response = self.client.post('/auth/login', json=login_data)
        token = json.loads(login_response.data)['access_token']

        check_response = self.client.get('/auth/check', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(check_response.status_code, 200)
        check_response_data = json.loads(check_response.data)
        self.assertIn('user', check_response_data)
        self.assertEqual(check_response_data['user']['username'], 'testuser')

    def test_check_token_invalid(self):
        check_response = self.client.get('/auth/check', headers={'Authorization': 'Bearer invalidtoken'})
        self.assertEqual(check_response.status_code, 401)

    def test_logout(self):
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_response = self.client.post('/auth/login', json=login_data)
        token = json.loads(login_response.data)['access_token']

        logout_response = self.client.post('/auth/logout', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(logout_response.status_code, 200)
        response_data = json.loads(logout_response.data)
        self.assertEqual(response_data['message'], 'Logged out successfully')

    def test_logout_no_token(self):
        logout_response = self.client.post('/auth/logout')
        self.assertEqual(logout_response.status_code, 401)