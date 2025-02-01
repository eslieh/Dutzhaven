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
            self.token = create_access_token(identity=self.test_user.id)

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
            'deadline': '2024-12-31'
        }
        response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Task created successfully')
        self.assertIn('task', response_data)
        self.assertEqual(response_data['task']['title'], 'Test Task')
        self.assertIsInstance(response_data['task']['id'], int)

        with self.app.app_context():
            task = Task.query.get(response_data['task']['id'])
            self.assertIsNotNone(task)
            self.assertEqual(task.title, 'Test Task')

    def test_create_task_missing_fields(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
        }
        response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Missing required fields')

    def test_create_task_invalid_budget(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 'abc',
            'deadline': '2024-12-31'
        }
        response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Invalid budget format')

    def test_get_tasks(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
            'deadline': '2024-12-31'
        }
        self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})

        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIsInstance(response_data, list)
        self.assertTrue(len(response_data) >= 1)
        task = response_data[0]
        self.assertIn('id', task)
        self.assertIn('title', task)
        self.assertIn('description', task)
        self.assertIn('category', task)
        self.assertIn('budget', task)
        self.assertIn('deadline', task)
        self.assertIn('status', task)
        self.assertIn('client_id', task)

    def test_get_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
            'deadline': '2024-12-31'
        }
        create_response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        task_id = json.loads(create_response.data)['task']['id']

        response = self.client.get(f'/tasks/{task_id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['title'], 'Test Task')

    def test_update_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
            'deadline': '2024-12-31'
        }
        create_response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        task_id = json.loads(create_response.data)['task']['id']

        updated_data = {'title': 'Updated Task Title', 'budget': 200.00}
        response = self.client.put(f'/tasks/{task_id}', json=updated_data, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            updated_task = Task.query.get(task_id)
            self.assertEqual(updated_task.title, 'Updated Task Title')
            self.assertEqual(updated_task.budget, 200.00)

    def test_update_task_unauthorized(self):
        hashed_password = generate_password_hash('otherpassword', method='sha256')
        other_user = User(username='otheruser', email='other@example.com', password_hash=hashed_password, user_type='client')
        with self.app.app_context():
            db.session.add(other_user)
            db.session.commit()
            other_token = create_access_token(identity=other_user.id)

            data = {
                'title': 'Test Task',
                'description': 'Test Description',
                'category': 'Test Category',
                'budget': 100.00,
                'deadline': '2024-12-31'
            }
            create_response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
            task_id = json.loads(create_response.data)['task']['id']

            updated_data = {'title': 'Updated Task Title'}
            response = self.client.put(f'/tasks/{task_id}', json=updated_data, headers={'Authorization': f'Bearer {other_token}'})
            self.assertEqual(response.status_code, 403)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['message'], 'You are not authorized to update this task')

    def test_delete_task(self):
        data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'category': 'Test Category',
            'budget': 100.00,
            'deadline': '2024-12-31'
        }
        create_response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
        task_id = json.loads(create_response.data)['task']['id']

        response = self.client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Task deleted successfully')

        with self.app.app_context():
            deleted_task = Task.query.get(task_id)
            self.assertIsNone(deleted_task)

    def test_delete_task_unauthorized(self):
        hashed_password = generate_password_hash('otherpassword', method='sha256')
        other_user = User(username='otheruser', email='other@example.com', password_hash=hashed_password, user_type='client')
        with self.app.app_context():
            db.session.add(other_user)
            db.session.commit()
            other_token = create_access_token(identity=other_user.id)

            data = {
                'title': 'Test Task',
                'description': 'Test Description',
                'category': 'Test Category',
                'budget': 100.00,
                'deadline': '2024-12-31'
            }
            create_response = self.client.post('/tasks/create', json=data, headers={'Authorization': f'Bearer {self.token}'})
            task_id = json.loads(create_response.data)['task']['id']

            response = self.client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {other_token}'})
            self.assertEqual(response.status_code, 403)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['message'], 'You are not authorized to delete this task')