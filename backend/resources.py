
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from models import db, User, Task, Bid
from config import Config
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
api = Api(app)

# Enable CORS for all routes (this will allow requests from any origin)
CORS(app)

# If you want to restrict to specific origins, you can do this instead:
# CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})

# Auth API
class AuthResource(Resource):
    def post(self, action):
        data = request.json
        if action == "register":
            new_user = User(
                full_name=data['full_name'],
                user_type=data['user_type'],
                username=data['username'],
                email=data['email'],
                password_hash=data['password']
            )
            db.session.add(new_user)
            db.session.commit()
            return {"message": "User registered successfully"}, 201

        elif action == "login":
            user = User.query.filter_by(username=data['username']).first()
            if user and user.password_hash == data['password']:
                # access_token = create_access_token(identity=user.id)
                return {"user_id": user.id}, 200
            return {"message": "Invalid credentials"}, 401

api.add_resource(AuthResource, "/auth/<string:action>")

# User API
class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return {"id": user.id, "username": user.username, "email": user.email}

    def post(self):
        data = request.json
        new_user = User(
            full_name=data['full_name'],
            user_type=data['user_type'],
            username=data['username'],
            email=data['email'],
            password_hash=data['password_hash']
        )
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully"}, 201

api.add_resource(UserResource, "/users/<int:user_id>", "/users")

# Task API
class TaskResource(Resource):
    def get(self, task_id):
        task = Task.query.get(task_id)
        if not task:
            return {"message": "Task not found"}, 404
        return {"id": task.id, "title": task.title, "status": task.status}

    def post(self):
        data = request.json
        new_task = Task(
            client_id=data['client_id'],
            title=data['title'],
            description=data['description'],
            category=data.get('category'),
            budget=data.get('budget'),
            deadline=data.get('deadline')
        )
        db.session.add(new_task)
        db.session.commit()
        return {"message": "Task created successfully"}, 201

api.add_resource(TaskResource, "/tasks/<int:task_id>", "/tasks")

# Bid API
class BidResource(Resource):
    def get(self, bid_id):
        bid = Bid.query.get(bid_id)
        if not bid:
            return {"message": "Bid not found"}, 404
        return {"id": bid.id, "task_id": bid.task_id, "price": bid.price}

    def post(self):
        data = request.json
        new_bid = Bid(
            task_id=data['task_id'],
            freelancer_id=data['freelancer_id'],
            proposal_text=data.get('proposal_text'),
            price=data.get('price')
        )
        db.session.add(new_bid)
        db.session.commit()
        return {"message": "Bid created successfully"}, 201

api.add_resource(BidResource, "/bids/<int:bid_id>", "/bids")

if __name__ == "__main__":
    app.run(debug=True)
