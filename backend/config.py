import os

class Config:
    SECRET_KEY = '74cd3fa84f617e25e62250f10a64bcb36a417f9e01f7c6ca949057f951c4dd90' 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = '981d53d62d97f82cf1ab2b492850a1947d9b263460216477cb40ffc27df88552' 
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DutzHaven.db'

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  
}