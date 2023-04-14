import logging
from http import HTTPStatus
from urllib.parse import urlparse

import folium
import httpx
from core.app.utils import get_country_code
from flask import abort
from flask import current_app
from flask import request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from . import main_bp

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@main_bp.get("/admin/")
@auth.login_required
def dashboard():
    return "Hello, %s!" % auth.current_user()


@main_bp.before_app_request
def check_access_endpoint():
    country = get_country_code()
    allowed_countries = current_app.config["ALLOWED_COUNTRIES"]
    if country not in allowed_countries:
        abort(HTTPStatus.FORBIDDEN, "Access denied")


@main_bp.route("/map/")
def map_view():

    api_url = request.url_root
    req_url = api_url + "api/pics/"

    try:
        with httpx.Client() as client:
            pics_response = client.get(req_url).json()
    except (httpx.RequestError, ValueError) as error:
        logger.debug(f"Error fetching pics data {error}")
        return "Error fetching pics data"

    if not pics_response:
        map = folium.Map(zoom_start=10)
    else:
        map = folium.Map(
            location=[
                pics_response[0]["longitude"],
                pics_response[0]["latitude"]
            ],
            zoom_start=10
        )
        for pic in pics_response:

            location = [pic.get("longitude"), pic.get("latitude")]
            name = f"{pic.get('name')} ({pic.get('altitude')} Km)"

            folium.Marker(
                location=location,
                popup=folium.Popup(name, parse_html=True),
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(map)


    map_html = map.get_root().render()
    return map_html
