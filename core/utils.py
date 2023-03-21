import requests


def get_address_id():
    url = 'https://api64.ipify.org?format=json'
    response = requests.get(url).json()
    ip = response.get("ip")
    return ip


def get_country_code():
    ip_address = get_address_id()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    country_code = response.get('country_code')
    return country_code
