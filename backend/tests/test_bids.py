import unittest
import json
from flask import create_app
from .. import db
from ..models import User, Task, Bid
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class BidTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app('config.TestConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            hashed_password = generate_password_hash('testpassword', method='sha256')
            self.test_client = User(username='testclient', email='client@example.com', password_hash=hashed_password, user_type='client')
            self.test_freelancer = User(username='testfreelancer', email='freelancer@example.com', password_hash=hashed_password, user_type='freelancer')
            db.session.add_all([self.test_client, self.test_freelancer])
            db.session.commit()
            self.client_token = create_access_token(identity=self.test_client.id)
            self.freelancer_token = create_access_token(identity=self.test_freelancer.id)

            # Create a test task
            self.test_task = Task(client_id=self.test_client.id, title='Test Task', description='Test', category='Test', budget=100, deadline='2024-12-31')
            db.session.add(self.test_task)
            db.session.commit()


    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_bid(self):
        data = {
            'proposal_text': 'Test Proposal',
            'price': 50.00
        }
        response = self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'Bid submitted successfully')

        with self.app.app_context():  # Check if the bid is in the database
            bid = Bid.query.filter_by(task_id=self.test_task.id, freelancer_id=self.test_freelancer.id).first()
            self.assertIsNotNone(bid)
            self.assertEqual(bid.price, 50.00)

    def test_create_bid_existing_bid(self): # Test creating a bid when one already exists
        data = {
            'proposal_text': 'Test Proposal',
            'price': 50.00
        }
        response = self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})
        self.assertEqual(response.status_code, 201) # First bid should be successful

        # Try creating another bid for the same task by the same freelancer
        response2 = self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})
        self.assertEqual(response2.status_code, 400)
        response_data2 = json.loads(response2.data)
        self.assertEqual(response_data2['message'], 'You have already submitted a bid for this task')


    def test_get_bids_for_task(self):
        # First, create a bid (as in test_create_bid)
        data = {
            'proposal_text': 'Test Proposal',
            'price': 50.00
        }
        self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})

        response = self.client.get(f'/bids/task/{self.test_task.id}')
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIsInstance(response_data, list)
        self.assertEqual(len(response_data), 1) # Check if one bid was returned
        self.assertEqual(response_data[0]['price'], 50.00) # Check bid price

    def test_update_bid(self):
        # ... (Create a bid first)
        data = {
            'proposal_text': 'Test Proposal',
            'price': 50.00
        }
        self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})


        updated_data = {
            'proposal_text': 'Updated Proposal',
            'price': 75.00
        }
        bid = Bid.query.filter_by(task_id=self.test_task.id, freelancer_id=self.test_freelancer.id).first()

        response = self.client.put(f'/bids/{bid.id}', json=updated_data, headers={'Authorization': f'Bearer {self.freelancer_token}'})
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            updated_bid = Bid.query.get(bid.id)
            self.assertEqual(updated_bid.price, 75.00) # Check if price updated

    def test_delete_bid(self):
        # ... (Create a bid first)
        data = {
            'proposal_text': 'Test Proposal',
            'price': 50.00
        }
        self.client.post(f'/bids/create/{self.test_task.id}', json=data, headers={'Authorization': f'Bearer {self.freelancer_token}'})
        bid = Bid.query.filter_by(task_id=self.test_task.id, freelancer_id=self.test_freelancer.id).first()

        response = self.client.delete(f'/bids/{bid.id}', headers={'Authorization': f'Bearer {self.freelancer_token}'})
        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            deleted_bid = Bid.query.get(bid.id)
            self.assertIsNone(deleted_bid) # Check if bid deleted