import json
from tests.base_case import BaseCase

from flask import url_for

from core import db
from core.app.models import Pic
from core.apis.pics import abort_if_pic_doesnt_exist


class TestPics(BaseCase):

    def test_get_all_pics(self):
        response = self.client.get('/api/pics/')
        self.assertEqual(response.status_code, 200)

    def test_create_pic(self):
        data = {'name': 'New Pic', 'latitude': 30.0, 'longitude': 40.0, 'altitude': 3000.0}
        response = self.client.post('/api/pics/', json=data)
        self.assertEqual(response.status_code, 201)

        pic = Pic.query.filter_by(name='New Pic').first()
        self.assertIsNotNone(pic)
        self.assertEqual(pic.latitude, 30.0)
        self.assertEqual(pic.longitude, 40.0)
        self.assertEqual(pic.altitude, 3000.0)

    def test_create_pic_invalid_data(self):
        data = {'name': 'New Pic', 'latitude': 30.0, 'altitude': 3000.0}
        response = self.client.post('/api/pics/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_create_pic_missing_data(self):
        data = {'name': 'New Pic', 'latitude': 30.0, 'longitude': 40.0}
        response = self.client.post('/api/pics/', json=data)
        self.assertEqual(response.status_code, 400)

    def test_get_pic(self):
        pic = Pic(name="New Pic", latitude=30.0, longitude=40.0, altitude=3000.0)
        pic.save()

        self.assertIsNotNone(abort_if_pic_doesnt_exist(pic.id))
        response = self.client.get(f'/api/pics/{pic.id}/')
        self.assertEqual(response.status_code, 200)

    def test_get_pic_nonexistent(self):
        response = self.client.get('/api/pics/99999/')
        self.assertEqual(response.status_code, 404)

    def test_pic_update(self):
        pic = Pic(name="Update Pic", latitude=30.0, longitude=40.0, altitude=3000.0)
        pic.save()
        data = {
            "name": "Update Pic",
            "latitude": 30.0,
            "longitude": 40.0,
            "altitude": 3000
        }

        updated_pic = abort_if_pic_doesnt_exist(pic.id)
        self.assertIsNotNone(updated_pic)

        response = self.client.patch(f'api/pics/{pic.id}/', json=data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(updated_pic.name, "Update Pic")
        self.assertEqual(updated_pic.latitude, 30.0)
        self.assertEqual(updated_pic.longitude, 40.0)
        self.assertEqual(updated_pic.altitude, 3000)

    def test_pic_delete(self):
        pic = Pic(name="Delete PIC", latitude=50.0, longitude=-120.0, altitude=1000)
        pic.save()

        # Check that the pic exists before deletion
        self.assertIsNotNone(abort_if_pic_doesnt_exist(pic.id))
        response = self.client.delete(f'api/pics/{pic.id}/')
        self.assertEqual(response.status_code, 200)

        # Check that the pic was actually deleted
        response = self.client.delete(f'api/pics/{pic.id}/')
        self.assertEqual(response.status_code, 404)

    def test_get_pics_in_range(self):

        pic1 = Pic(name='Pic1', latitude=48.5, longitude=2.5, altitude=100)
        pic2 = Pic(name='Pic2', latitude=49.0, longitude=2.0, altitude=200)
        pic3 = Pic(name='Pic3', latitude=80.5, longitude=4.5, altitude=300)
        db.session.add_all([pic1, pic2, pic3])
        db.session.commit()

        response = self.client.get('/api/pics/48.0/50.0/2.0/3.0/')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data.decode())
        self.assertEqual(len(data), 2)

        pic_names = [pic['name'] for pic in data]
        self.assertIn('Pic1', pic_names)
        self.assertIn('Pic2', pic_names)

    def test_get_pics_in_range_no_results(self):
        response = self.client.get('/api/pics/50.0/52.0/2.0/3.0/')
        self.assertEqual(response.status_code, 404)
