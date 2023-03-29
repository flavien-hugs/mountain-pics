from flask import Blueprint
from flask_restx import Api

api_bp = Blueprint("api_bp", __name__, url_prefix="/api/")

api = Api(
    api_bp, version="1.0",
    title="Mountain API",
    ordered=True,
    description="API to store and retrieve mountains data"
)

from . import pics
