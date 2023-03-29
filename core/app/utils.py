import logging
import requests

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_address_ip():
    try:
        url = 'https://api64.ipify.org?format=json'
        response = requests.get(url)
        ip = response.json().get("ip")
        if not ip or not isinstance(ip, str):
            raise ValueError("Invalid IP address")
        return ip
    except (requests.exceptions.RequestException, ValueError) as error:
        logger.debug(f"Unable to obtain IP address: {error})")
        return None


def get_country_code():
    try:
        ip_address = get_address_ip()
        if not ip_address:
            return None
        url = f"https://ipapi.co/{ip_address}/json/"
        response = requests.get(url)
        country_code = response.json().get("country_code")
        if not country_code or not isinstance(country_code, str):
            raise ValueError("Invalid country code")
        return country_code
    except (requests.exceptions.RequestException, ValueError) as error:
        logger.debug(f"Unable to obtain the country code: {error})")
        return None
