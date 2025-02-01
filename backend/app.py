import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .config import config


db = SQLAlchemy() 

migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from .routes import auth_bp, tasks_bp, users_bp, bids_bp, messages_bp, reviews_bp
    from .models import User, Task, Bid, Message, Review
    

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(bids_bp, url_prefix='/bids')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    return app

config_name = os.getenv('FLASK_CONFIG') or 'default'
app = create_app(config[config_name])

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return "Welcome to DutzHaven Backend API!"

for rule in app.url_map.iter_rules():
    print(rule)

if __name__ == '__main__':
    app.run(debug=True)