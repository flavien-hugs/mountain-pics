from datetime import timedelta

from flask import abort, jsonify, request, current_app

from http import HTTPStatus
from flask_restx import Resource
from core import db

from . import api
from core.app.models import Pic
from core.apis.resources import pic_fields, geo_bounding_box

pic_ns = api.namespace('pics', description="A namespace for operation pics")


def abort_if_pic_doesnt_exist(pic_id: int) -> Pic:
    pic = Pic.query.get(pic_id)
    if not pic:
        abort(HTTPStatus.NOT_FOUND, f"Could not find pic with id {pic_id}")
    return pic


@pic_ns.route('/')
class PicList(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.FORBIDDEN): "Access denied",
            int(HTTPStatus.NOT_FOUND): "Pics not found",
        }
    )
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
        },
        body=pic_fields
    )
    @pic_ns.expect(pic_fields)
    def post(self):

        """
        endpoint to create a pic
        """

        data = request.json

        # Validate input data
        if not all(key in data for key in ['name', 'latitude', 'longitude', 'altitude']):
            return jsonify({"error": "Invalid input data"}), HTTPStatus.BAD_REQUEST

        new_pic = Pic(
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude")
        )
        new_pic.save()

        response_data = {
            "message": "New pic created successfully",
            "pic": new_pic.to_json()
        }
        return jsonify(response_data), HTTPStatus.CREATED


@pic_ns.route("/<int:pic_id>/")
class PicDetail(Resource):

    @pic_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Pic not found",
        }
    )
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
        body=pic_fields
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
            "pics": [pic.to_json() for pic in pics]
        }

        return response_data, HTTPStatus.OK


@pic_ns.route('/location')
class PicsList(Resource):

    @pic_ns.expect(geo_bounding_box)
    @pic_ns.doc('geo_bounding_box')
    def post(self):

        '''
        List all pics in a given location
        '''

        data = request.json

        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # db.func.cast() pour extraire les valeurs
        # de Pic.latitude et Pic.longitude en tant que flottants,

        pic_latitude = db.func.cast(Pic.latitude, db.Float)
        pic_longitude = db.func.cast(Pic.longitude, db.Float)

        # Utilisation de db.func.power() pour élever chaque terme au carré
        sqrt_lat = db.func.power(latitude - pic_latitude, 2)
        sqrt_lon = db.func.power(longitude - pic_longitude, 2)

        # db.func.sqrt() pour calculer de la distance entre les points .
        distance_between = db.func.sqrt(sqrt_lat + sqrt_lon)

        pics = Pic.query.filter(distance_between).all()

        return [pic.to_json() for pic in pics]
