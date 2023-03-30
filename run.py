import logging as lg
import os
import json

from dotenv import dotenv_values
from flask_migrate import Migrate
from flask_migrate import upgrade

from core import db, create_mountain_app
from core.app.models import Pic

env = dotenv_values(".flaskenv")

mountain_app = create_mountain_app(env.get("FLASK_CONFIG") or "dev")
migrate = Migrate(mountain_app, db, render_as_batch=True)

@mountain_app.shell_context_processor
def make_shell_context():
    return dict(db=db, Pic=Pic)


@mountain_app.cli.command("init_db")
def init_db():
    upgrade()
    db.create_all()
    db.session.commit()
    lg.warning("Database initialized !")


if __name__ == "__main__":
    mountain_app.run(port=5000, host="0.0.0.0")
