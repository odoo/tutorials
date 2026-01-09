import json
from odoo.tests.common import HttpCase


class TestCustomAuthSignup(HttpCase):
    def test_01_home_page_loads(self):
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)

    def test_02_web_signup_route_loads(self):
        response = self.url_open("/web/signup")
        self.assertEqual(response.status_code, 200)

    def test_03_duplicate_email_signup(self):
        existing_user_data = {
            "name": "Existing User",
            "login": "existinguser@example.com",
            "password": "ExistingPass123",
            "confirm_password": "ExistingPass123",
        }
        user_data_db = existing_user_data.copy()
        del user_data_db["confirm_password"]
        self.env["res.users"].create(user_data_db)
        response = self.url_open("/web/signup/res.users", data=existing_user_data)
        response_data = json.loads(response.text)

        self.assertIn("error", response_data)
        self.assertEqual(
            response_data["error"],
            "Another user is already registered using this email address.",
        )

    def test_04_password_mismatch(self):
        mismatched_password_data = {
            "name": "New User",
            "login": "newuser@example.com",
            "password": "Password123",
            "confirm_password": "WrongPassword123",
        }

        response = self.url_open("/web/signup/res.users", data=mismatched_password_data)
        response_data = json.loads(response.text)

        self.assertIn("error", response_data)
        self.assertEqual(
            response_data["error"], "Passwords do not match; please retype them."
        )
