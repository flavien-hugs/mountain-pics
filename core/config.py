import os
from dotenv import dotenv_values

env = dotenv_values(".flaskenv")

DATABASE_URI = env.get("DATABASE_URL")

if DATABASE_URI.startswith("postgres://"):
    DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)

class Config:

    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SITE_NAME = "Mountain Pic"

    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = DATABASE_URI

    RESTX_VALIDATE = True
    HTTPAUTH_ENABLED = True

    ALLOWED_COUNTRIES = ['FR', 'US', 'CI']

    @staticmethod
    def init_app(mountain_app):
        pass


class DevConfig(Config):

    DEBUG = True
    DEVELOPMENT = True

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

class ProdConfig(Config):

    @classmethod
    def init_app(cls, mountain_app):
        Config.init_app(mountain_app)


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "test": TestConfig
}
