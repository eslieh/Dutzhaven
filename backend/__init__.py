import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:  # Or just use config_class as the parameter directly
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY') or 'your_secret_key',  # **Change this!**
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///haven.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'  # **Change this!**
        )
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)  # No need to assign to a variable unless you need to customize it

    from .routes import auth_bp, tasks_bp, users_bp, bids_bp, messages_bp, reviews_bp # Correct import

    app.register_blueprint(auth_bp, url_prefix='/auth')  # Add URL prefixes! (Important)
    app.register_blueprint(tasks_bp, url_prefix='/tasks')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(bids_bp, url_prefix='/bids')
    app.register_blueprint(messages_bp, url_prefix='/messages')
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    return app