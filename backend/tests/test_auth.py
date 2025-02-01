import unittest
import json
from flask import create_app
from .. import db
from ..models import User
from werkzeug.security import generate_password_hash

class AuthTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestConfig')  # Use a test config
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()  # Create tables for testing
            # Create a test user (optional)
            hashed_password = generate_password_hash('testpassword', method='sha256')
            test_user = User(username='testuser', email='test@example.com', password_hash=hashed_password, user_type='client')
            db.session.add(test_user)
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

        # Check if the user is in the database
        with self.app.app_context():
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)

    def test_register_duplicate_username(self):
        data = {
            'username': 'testuser',  # Existing user
            'email': 'diff@example.com',
            'password': 'password123',
            'user_type': 'client'
        }
        response = self.client.post('/auth/register', json=data)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Username already exists')

    # ... (Add more tests for register - missing fields, etc.)

    def test_login(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)  # Check for token

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post('/auth/login', json=data)
        self.assertEqual(response.status_code, 401)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Invalid credentials')

    def test_check_token(self):
        # First, log in to get a token
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_response = self.client.post('/auth/login', json=login_data)
        token = json.loads(login_response.data)['access_token']

        # Now, use the token to check
        check_response = self.client.get('/auth/check', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(check_response.status_code, 200)

    def test_logout(self):
        # First, log in to get a token
        login_data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        login_response = self.client.post('/auth/login', json=login_data)
        token = json.loads(login_response.data)['access_token']

        # Now, use the token to logout
        logout_response = self.client.post('/auth/logout', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(logout_response.status_code, 200)
        response_data = json.loads(logout_response.data)
        self.assertEqual(response_data['message'], 'Logged out successfully')

