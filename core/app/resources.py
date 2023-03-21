from flask_restx import fields
from app import api


pic_fields = api.model(
    "Pic",
    {
        "id": fields.Integer(readonly=True, description="Pic id"),
        "name": fields.String(
            required=True, description="The pic name"
        ),
        "latitude": fields.String(
            required=True, description="The pic latitude"
        ),
        "longitude": fields.String(
            required=True, description="The pi latitude"
        ),
        "altitude": fields.String(
            required=True, description="The pic altitude"
        ),
        "created_at": fields.DateTime(
            readonly=True, description="The pic created date"
        ),
        "updated_at": fields.DateTime(
            readonly=True, description="The pic updated date"
        ),
    },
)
