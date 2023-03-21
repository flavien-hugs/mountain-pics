from flask import Blueprint, request, render_template

import folium
import requests

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import Pic

main_bp = Blueprint("main_bp", __name__, url_prefix="/")


auth = HTTPBasicAuth()

users = {
    "admin": generate_password_hash("admin"),
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@main_bp.route('/map/')
def map_view():

    api_url = request.url_root
    req_url = api_url + "pics"
    response = requests.request("GET", req_url).json()
    map = folium.Map(zoom_start=13)

    for pic in response:
        folium.Marker(
            location=[pic['latitude'], pic['longitude']],
            popup=folium.Popup(pic['name'], parse_html=True),
            icon=folium.Icon(color="red", icon="info-sign"),
        ).add_to(map)

    map_html = map.get_root().render()
    return map_html


@main_bp.route('/admin/')
@auth.login_required
def dashboard():
    return "Hello, %s!" % auth.current_user()
