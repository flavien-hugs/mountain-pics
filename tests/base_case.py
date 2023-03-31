import sys
import unittest

from core import create_mountain_app
from core import db
from flask import current_app


sys.path.append("..")


class BaseCase(unittest.TestCase):
    def setUp(self):
        self.app = create_mountain_app("test")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config["TESTING"])


if __name__ == "__main__":
    unittest.main()
