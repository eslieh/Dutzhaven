import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_secret_key'  # **CHANGE THIS!**
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///haven.db'  # Or your PostgreSQL/MySQL URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppress SQLAlchemy warnings
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'your_jwt_secret_key'  # **CHANGE THIS!**
    # ... other configuration variables as needed (e.g., for payment gateways, email, etc.)

class DevelopmentConfig(Config):
    DEBUG = True  # Enable debugging in development

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing

class ProductionConfig(Config):
    # Production-specific settings (e.g., different database URI, logging, etc.)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@host:port/database' # Example for PostgreSQL
    DEBUG = False
    # ... other production settings