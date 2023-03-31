from flask_restx import fields

from . import api


pic_fields = api.model(
    "Pic",
    {
        "id": fields.Integer(readonly=True, description="Pic identifier"),
        "name": fields.String(required=True, description="The pic name"),
        "latitude": fields.Float(required=True, description="The pic latitude"),
        "longitude": fields.Float(required=True, description="The pi latitude"),
        "altitude": fields.Float(required=True, description="The pic altitude"),
    },
)
