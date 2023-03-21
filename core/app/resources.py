from flask_restx import fields
from app import api


peak_create_fields = api.model(
    "PeakCreate",
    {
        "id": fields.Integer(readonly=True, description="Peak id"),
        "name": fields.String(
            required=True, description="Peak name"
        ),
        "latitude": fields.String(
            required=True, description="Peak latitude"
        ),
        "longitude": fields.String(
            required=True, description="Peak latitude"
        ),
        "altitude": fields.String(
            required=True, description="Peak altitude"
        ),
    },
)


peak_fields = api.model(
    "Peak",
    {
        "id": fields.Integer(readonly=True, description="Peak id"),
        "name": fields.String(
            required=True, description="Peak name"
        ),
        "latitude": fields.Float(
            required=True, description="Peak latitude"
        ),
        "longitude": fields.Float(
            required=True, description="Peak latitude"
        ),
        "altitude": fields.Float(
            required=True, description="Peak altitude"
        ),
        "created_at": fields.DateTime(
            required=True, description="Peak created date"
        ),
    },
)
