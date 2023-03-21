from datetime import timedelta
from http import HTTPStatus

from flask import jsonify
from flask import request

from flask_restx import Resource
from app import api
from app.models import Peak
from app.resources import peak_create_fields, peak_fields


peak_ns = api.namespace(
    "peaks", version="1.0",
    description="A namespace for operation peak"
)

def abort_if_peak_doesnt_exist(id):
    if id not in Peak.query.all():
        return jsonify(
            {"success": True, "message": f"Could not find peak with that {id}"}
        )

@peak_ns.route('/')
class PeakCreateResource(Resource):
    @peak_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Peak not found"
        }
    )
    def get(self):
        """
        Peak list
        """
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        peaks = Peak.query.order_by(Peak.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return [peak.to_json() for peak in peaks.items]
