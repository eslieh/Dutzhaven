import unittest
import json
from flask import create_app
from .. import db
from ..models import User, Task
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class TaskTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed_password = generate_password_hash('testpassword', method='sha256')
            self.test_user = User(username='testuser', email='test@example.com', password_hash=hashed_password, user_type='client')
            db.session.add(self.test_user)
            db.session.commit()
            self.token = create_access_token(identity=self.test_user.id) # Generate token for testing

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
            'deadline': '2024-12-31'  # ISO 8601 format
        }
        response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Task created successfully')
        self.assertIn('task_id', response_data)

        with self.app.app_context():
            task = Task.query.get(response_data['task_id'])
            self.assertIsNotNone(task)
            self.assertEqual(task.title, 'Test Task')

    # ... (Add more tests for create_task - missing fields, invalid data, etc.)

    def test_get_tasks(self):
        # First, create a task (as in test_create_task)
        # ... (Code to create a task)

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIsInstance(response_data, list) # Check if it's a list of tasks
        # ... (Add assertions to check the content of the task list)

    def test_get_task(self):
        # ... (Create a task first)
        response = self.client.get('/tasks/1')  # Replace 1 with the actual task ID
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['title'], 'Test Task') # Check if the task title is correct

    def test_update_task(self):
        # ... (Create a task first)
        updated_data = {'title': 'Updated Task Title'}
        response = self.client.put('/tasks/1', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        # ... (Check if the task was updated in the database)

    def test_delete_task(self):
        # ... (Create a task first)
        response = self.client.delete('/tasks/1', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        # ... (Check if the task was deleted from the database)