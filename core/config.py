import os

DATABASE_URL='postgresql://mountain:mountain@localhost/mountain_pics_db'

class Config:

    DEBUG = False
    DEVELOPMENT = False

    SITE_NAME = "Mountain Pic"

    SECRET_KEY = os.getenv("SECRET_KEY", os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    RESTX_VALIDATE = True
    HTTPAUTH_ENABLED = True

    ALLOWED_COUNTRIES = ['Fr', 'US', 'CI']

    @staticmethod
    def init_app(mountain_app):
        pass


class DevConfig(Config):

    DEBUG = True
    DEVELOPMENT = True

class ProdConfig(Config):

    @classmethod
    def init_app(cls, mountain_app):
        Config.init_app(mountain_app)


config = {
    "dev": DevConfig,
    "prod": ProdConfig,
}
