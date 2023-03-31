from dotenv import dotenv_values

env = dotenv_values(".flaskenv")

DATABASE_URI = "postgresql://mountain:mountain@localhost/mountain_pics_db"


class Config:

    DEBUG = False
    TESTING = False
    DEVELOPMENT = False

    SITE_NAME = "Mountain Pic"

    SECRET_KEY = env.get("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = DATABASE_URI

    RESTX_VALIDATE = True
    HTTPAUTH_ENABLED = True

    ALLOWED_COUNTRIES = ["FR", "US", "CI"]

    @staticmethod
    def init_app(mountain_app):
        pass


class DevConfig(Config):

    DEBUG = True
    DEVELOPMENT = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProdConfig(Config):
    @classmethod
    def init_app(cls, mountain_app):
        Config.init_app(mountain_app)


config = {"dev": DevConfig, "prod": ProdConfig, "test": TestConfig}
