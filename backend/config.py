import os

class Config:
    SECRET_KEY = '74cd3fa84f617e25e62250f10a64bcb36a417f9e01f7c6ca949057f951c4dd90' # **CHANGE THIS!**
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '981d53d62d97f82cf1ab2b492850a1947d9b263460216477cb40ffc27df88552'  # **CHANGE THIS!**

    # Base Database Configuration (for potential production override)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')  # For production override

    @staticmethod
    def init_app(app):
        pass  # Can be used for environment-specific initialization

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DutzHaven.db'  # Development SQLite database (relative path)
    # SQLALCHEMY_ECHO = True  # Optional: to see SQL queries in the console

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing

class ProductionConfig(Config):
    # For production, you *could* still use SQLite, but it's generally not recommended for large-scale apps
    # If you use a different DB in production, uncomment and adjust the following:
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://user:password@host:port/database_name'  # Or MySQL
    DEBUG = False
    # ... other production settings (e.g., logging)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Default environment
}