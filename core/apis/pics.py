from http import HTTPStatus

from core import db
from core.apis.resources import pic_fields
from core.app.models import Pic
from flask import abort
from flask import jsonify
from flask import request
from flask_restx import Resource

from . import api

pic_ns = api.namespace("pics", description="A namespace for operation pics")


def abort_if_pic_doesnt_exist(pic_id: int) -> Pic:
    pic = Pic.query.filter_by(id=pic_id).first()
    if not pic:
        abort(HTTPStatus.NOT_FOUND, f"Could not find pic with id {pic_id}")
    return pic


@pic_ns.route("/")
class PicList(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.FORBIDDEN): "Access denied",
            int(HTTPStatus.NOT_FOUND): "Pics not found",
        }
    )
    @pic_ns.marshal_list_with(pic_fields)
    def get(self):

        """
        endpoint to read all pics
        """

        pics = Pic.query.all()
        return [pic.to_json() for pic in pics]

    @pic_ns.doc(
        responses={
            int(HTTPStatus.FORBIDDEN): "Access denied",
            int(HTTPStatus.CREATED): "New pic created successfully",
        }
    )
    @pic_ns.expect(pic_fields)
    def post(self):

        """
        endpoint to create a pic
        """

        data = request.json

        # Validate input data
        if not all(
            key in data for key in ["name", "latitude", "longitude", "altitude"]
        ):
            return jsonify({"error": "Invalid input data"}), HTTPStatus.BAD_REQUEST

        new_pic = Pic(
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude"),
        )
        new_pic.save()

        response_data = {
            "message": "New pic created successfully",
            "pic": new_pic.to_json(),
        }
        return response_data, HTTPStatus.CREATED


@pic_ns.route("/<int:pic_id>/")
class PicDetail(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Pic not found",
        }
    )
    @pic_ns.marshal_with(pic_fields)
    def get(self, pic_id):

        """
        endpoint to retrieve a pic by id
        """

        pic = abort_if_pic_doesnt_exist(pic_id)

        return pic.to_json()

    @pic_ns.doc(
        responses={
            int(HTTPStatus.UNAUTHORIZED): "User logged required",
            int(HTTPStatus.NOT_FOUND): "Pic not found",
            int(HTTPStatus.OK): "Pic updated successfully",
        },
    )
    @pic_ns.expect(pic_fields)
    def patch(self, pic_id):

        """
        endpoint to update a peak by id
        """

        data = request.json
        pic = abort_if_pic_doesnt_exist(pic_id)

        pic.name = data.get("name")
        pic.latitude = data.get("latitude")
        pic.longitude = data.get("longitude")
        pic.altitude = data.get("altitude")
        pic.save()

        return pic.to_json(), HTTPStatus.OK

    @pic_ns.doc(
        responses={
            int(HTTPStatus.UNAUTHORIZED): "User logged required",
            int(HTTPStatus.NOT_FOUND): "Pic not found",
            int(HTTPStatus.OK): "Pic deleted successfully",
        },
    )
    def delete(self, pic_id):

        """
        endpoint to delete a pic by id
        """

        pic = abort_if_pic_doesnt_exist(pic_id)

        pic.remove()

        pics = Pic.query.all()

        response_data = {
            "message": "Pic deleted successfully",
            "pics": [pic.to_json() for pic in pics],
        }

        return response_data, HTTPStatus.OK


@pic_ns.route("/<float:min_lat>/<float:max_lat>/<float:min_lon>/<float:max_lon>/")
@pic_ns.doc(
    params={
        "min_lat": "Minimum latitude",
        "max_lat": "Maximum latitude",
        "min_lon": "Minimum longitude",
        "max_lon": "Maximum longitude",
    }
)
class SearchPics(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.FORBIDDEN): "Access denied",
            int(HTTPStatus.NOT_FOUND): "Pics not found",
        }
    )
    @pic_ns.marshal_with(pic_fields, as_list=True)
    def get(self, min_lat, max_lat, min_lon, max_lon):

        try:
            pics = Pic.query.filter(
                Pic.latitude >= min_lat,
                Pic.latitude <= max_lat,
                Pic.longitude >= min_lon,
                Pic.longitude <= max_lon,
            ).all()
            if not pics:
                return {"message": "Pics not found"}, HTTPStatus.NOT_FOUND
            return [pic.to_json() for pic in pics]

        except db.exc.SQLAlchemyError:
            return {
                "message": "Internal server error"
            }, HTTPStatus.INTERNAL_SERVER_ERROR
