from datetime import timedelta
from http import HTTPStatus

from flask import jsonify
from flask import abort
from flask import request, current_app

from flask_restx import Resource
from app import api, db
from app.models import Pic
from app.resources import pic_fields, geo_bounding_box

from app.utils import get_country_code


pic_ns = api.namespace(
    "pics", version="1.0",
    description="A namespace for operation pic"
)

def abort_if_pic_doesnt_exist(id):
    if id not in Pic.query.all():
        return jsonify(
            {"success": True, "message": f"Could not find pic with that {id}"}
        )


def check_access_endpoint():
    country = get_country_code()
    if country not in current_app.config['ALLOWED_COUNTRIES']:
        abort(HTTPStatus.FORBIDDEN, 'Access denied')


@pic_ns.route('/')
class PicList(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.FORBIDDEN): "Access denied",
            int(HTTPStatus.NOT_FOUND): "Pics not found",
        }
    )
    def get(self):
        """endpoint to read all pics"""

        check_access_endpoint()

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

        """endpoint to create a pic"""

        check_access_endpoint()

        data = request.json

        new_pic = Pic(
            name=data.get("name"),
            latitude=data.get("latitude"),
            longitude=data.get("longitude"),
            altitude=data.get("altitude")
        )
        new_pic.save()

        response = new_pic.to_json()
        return response, HTTPStatus.CREATED


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

        check_access_endpoint()

        pic = Pic.query.get(pic_id)
        if not pic:
            abort_if_pic_doesnt_exist(id)
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

        """endpoint to update a peak by id"""

        check_access_endpoint()
        abort_if_pic_doesnt_exist(pic_id)

        data = request.json
        pic = Pic.query.get(pic_id)
        pic.name = data.get("name")
        pic.latitude = data.get("latitude")
        pic.longitude = data.get("longitude")
        pic.altitude = data.get("altitude")
        pic.save()

        return pic.to_json(), HTTPStatus.CREATED

    @pic_ns.doc(
        responses={
            int(HTTPStatus.UNAUTHORIZED): "User logged required",
            int(HTTPStatus.NOT_FOUND): "Pic not found",
            int(HTTPStatus.OK): "Pic deleted successfully",
        },
    )
    def delete(self, pic_id):

        """endpoint to delete a pic by id"""

        check_access_endpoint()

        pic = Pic.query.get(id=pic_id)
        if not need:
            abort_if_pic_doesnt_exist(pic_id)

        pic.remove()

        pics = Pic.query.all()

        return jsonify({
            "message": "Pic deleted successfully",
            "pics": [pic.to_json() for pic in pics]
        }), HTTPStatus.OK


@pic_ns.route('/location')
class PicsList(Resource):
    @pic_ns.expect(geo_bounding_box)
    @pic_ns.doc('geo_bounding_box')
    def post(self):

        '''List all pics in a given location'''

        check_access_endpoint()
        data = request.json

        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        radius = float(data.get('radius'))

        # db.func.cast() pour extraire les valeurs
        # de Pic.latitude et Pic.longitude en tant que flottants,

        pic_latitude = db.func.cast(Pic.latitude, db.Float)
        pic_longitude = db.func.cast(Pic.longitude, db.Float)

        # Utilisation de db.func.power() pour élever chaque terme au carré
        sqrt_lat = db.func.power(latitude - pic_latitude, 2)
        sqrt_lon = db.func.power(longitude - pic_longitude, 2)

        # db.func.sqrt() pour calculer de la distance entre les points .
        distance_between = db.func.sqrt(sqrt_lat + sqrt_lon)

        pics = Pic.query.filter(distance_between <= radius).all()

        return [pic.to_json() for pic in pics]