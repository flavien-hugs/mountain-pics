from flask import Flask

from flask_cors import CORS
from flask_restx import Api
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth

from app.config import config

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

cors = CORS()
migrate = Migrate()
auth = HTTPTokenAuth('Bearer')
db = SQLAlchemy(metadata=metadata)

api = Api(
    version="1.0",
    title="Mountain Pic API",
    description="A Mountain Pic API",
)

def create_mountain_app(config_name):

    mountain_app = Flask(__name__, instance_relative_config=True)
    mountain_app.config.from_object(config[config_name])
    config[config_name].init_app(mountain_app)

    api.init_app(mountain_app)
    migrate.init_app(mountain_app, db)
    db.init_app(mountain_app)
    cors.init_app(mountain_app, origins="*", supports_credentials=True)

    with mountain_app.app_context():

        from app.views import peak_ns

        if not mountain_app.debug:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = RotatingFileHandler(
                "logs/logging.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)

            mountain_app.logger.addHandler(file_handler)
            mountain_app.logger.setLevel(logging.INFO)
            mountain_app.logger.info("running mountain app")

        return mountain_app
