from datetime import timedelta
from http import HTTPStatus

from flask import jsonify
from flask import request

from flask_restx import Resource
from app import api, auth
from app.models import Pic
from app.resources import pic_fields


pic_ns = api.namespace(
    "pics", version="1.0",
    description="A namespace for operation pic"
)

def abort_if_pic_doesnt_exist(id):
    if id not in Pic.query.all():
        return jsonify(
            {"success": True, "message": f"Could not find pic with that {id}"}
        )

@pic_ns.route('/')
class PicList(Resource):
    @pic_ns.doc(
        responses={
            int(HTTPStatus.NOT_FOUND): "Pics not found",
        }
    )
    def get(self):
        """endpoint to read all pics"""

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        pics = Pic.query.order_by(Pic.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        return [pic.to_json() for pic in pics.items]


    @pic_ns.doc(
        responses={
            int(HTTPStatus.UNAUTHORIZED): "User logged required",
            int(HTTPStatus.CREATED): "New pic created successfully",
        },
        body=pic_fields
    )
    @auth.login_required
    @pic_ns.expect(pic_fields)
    def post(self):

        """endpoint to create a pic"""

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
    @auth.login_required
    def patch(self, pic_id):

        """endpoint to update a peak by id"""

        abort_if_pic_doesnt_exist(pic_id)

        data = request.json
        pic = Pic.query.get(pic_id)
        pic.name = data.get("name")
        pic.latitude = data.get("latitude")
        pic.longitude = data.get("longitude")
        pic.altitude = data.get("altitude")
        pic.save()

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Pic update successfully",
                    "pic": pic.to_json(),
                }
            ),
            HTTPStatus.CREATED
        )

    @pic_ns.doc(
        responses={
            int(HTTPStatus.UNAUTHORIZED): "User logged required",
            int(HTTPStatus.NOT_FOUND): "Pic not found",
            int(HTTPStatus.OK): "Pic deleted successfully",
        },
    )
    @auth.login_required
    def delete(self, pic_id):

        """endpoint to delete a pic by id"""

        pic = Pic.query.get(id=pic_id)
        if not need:
            abort_if_pic_doesnt_exist(pic_id)

        pic.remove()

        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        pics = Pic.query.order_by(Pic.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return (
            jsonify(
                {
                    "success": True,
                    "message": "Pic deleted successfully",
                    "pics": [pic.to_json() for pic in pics.items],
                }
            ),
            HTTPStatus.OK,
        )
