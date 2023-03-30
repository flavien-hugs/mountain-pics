from unittest.mock import patch
from tests.base_case import BaseCase

from base64 import b64encode


class TestApp(BaseCase):

    @patch('requests.get')
    def test_map_view(self, mock_get):
        mock_get.return_value.json.return_value = [
            {
                'longitude': 10.0,
                'latitude': 20.0,
                'name': 'Pic 1',
                'altitude': 1000,
            },
            {
                'longitude': 15.0,
                'latitude': 25.0,
                'name': 'Pic 2',
                'altitude': 2000,
            },
        ]

        response = self.client.get('/map/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_route_without_authentication(self):
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 401)

    def test_dashboard_route_with_authentication(self):
        username = "admin"
        password = "admin"

        response = self.client.get('/admin/', headers={
            'Authorization': 'Basic '+ b64encode(f"{username}:{password}".encode()).decode()
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello, admin!', response.data)
