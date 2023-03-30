from flask import request, current_app, abort

import folium
import requests

from http import HTTPStatus
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from . import main_bp
from core.app.models import Pic
from core.app.utils import get_country_code


auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
}


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username


@main_bp.before_app_request
def check_access_endpoint():
    country = get_country_code()
    allowed_countries = current_app.config['ALLOWED_COUNTRIES']
    if country not in allowed_countries:
        abort(HTTPStatus.FORBIDDEN, 'Access denied')


@main_bp.route("/map/")
def map_view():

    api_url = request.url_root
    req_url = api_url + "api/pics"
    pics_response = requests.get(req_url).json()

    map = folium.Map(zoom_start=13)
    for pic in pics_response:

        location = [pic.get('longitude'), pic.get('latitude')]
        name = f"{pic.get('name')} ({pic.get('altitude')} Km)"

        if location[0] is not None and location[1] is not None:
            folium.Marker(
                location=location,
                popup=folium.Popup(name, parse_html=True),
                icon=folium.Icon(color="red", icon="info-sign"),
            ).add_to(map)

    map_html = map.get_root().render()
    return map_html


@main_bp.get('/admin/')
@auth.login_required
def dashboard():
    return "Hello, %s!" % auth.current_user()
