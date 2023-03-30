import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, redirect, url_for

from flask_cors import CORS
from sqlalchemy import MetaData
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from core.config import config

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
db = SQLAlchemy(metadata=metadata)


def create_mountain_app(config_name):

    mountain_app = Flask(__name__, instance_relative_config=True)
    mountain_app.config.from_object(config[config_name])
    config[config_name].init_app(mountain_app)

    mountain_app.url_map.strict_slashes = False

    cors.init_app(mountain_app, origins="*", supports_credentials=True)

    db.init_app(mountain_app)
    migrate.init_app(mountain_app, db)

    with mountain_app.app_context():

        from core.apis import api_bp
        from core.app import main_bp

        mountain_app.register_blueprint(api_bp)
        mountain_app.register_blueprint(main_bp)

        @mountain_app.route("/")
        def entrypoint():
            return redirect(url_for("main_bp.map_view"))

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
