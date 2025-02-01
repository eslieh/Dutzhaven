import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class=None):
    app = Flask(__name__)

    if config_class is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY') or 'your_secret_key',
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///haven.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'
        )
    else:
        app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    JWTManager(app)

    from .routes import auth_bp, tasks_bp, users_bp, bids_bp, messages_bp, reviews_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(bids_bp)
    app.register_blueprint(messages_bp)
    app.register_blueprint(reviews_bp)

    return app