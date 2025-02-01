from . import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    bio = db.Column(db.Text)
    contact_info = db.Column(db.Text)
    profile_picture = db.Column(db.String(255))
    registration_date = db.Column(db.DateTime, default=datetime.utcnow)
    tasks = db.relationship('Task', backref='client', lazy=True)
    bids = db.relationship('Bid', backref='freelancer', lazy=True)
    messages_sent = db.relationship('Message', foreign_keys=[db.ForeignKey('message.sender_id')], backref='sender', lazy=True)
    messages_received = db.relationship('Message', foreign_keys=[db.ForeignKey('message.receiver_id')], backref='receiver', lazy=True)
    reviews_given = db.relationship('Review', foreign_keys=[db.ForeignKey('review.reviewer_id')], backref='reviewer', lazy=True)
    reviews_received = db.relationship('Review', foreign_keys=[db.ForeignKey('review.reviewee_id')], backref='reviewee', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100))
    budget = db.Column(db.Float)
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default='open')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    bids = db.relationship('Bid', backref='task', lazy=True)
    reviews = db.relationship('Review', backref='task', lazy=True)

class Bid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    freelancer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    proposal_text = db.Column(db.Text)
    price = db.Column(db.Float)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'), nullable=False)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    reviewee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)