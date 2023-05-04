from unittest import main, TestCase
from requests import get
import base64
from api.v1.auth.basic_auth import BasicAuth
from models.user import User
from functools import wraps
from json import dumps

test_email = "bob@hbtn.io"
test_pwd = "H0lbertonSchool98!"
token = base64.b64encode("{}:{}".format(
    test_email, test_pwd).encode("utf-8")).decode("utf-8")


class TestForUsersApi(TestCase):
    def setUp(self) -> None:
        self.url = "http://0.0.0.0:5000/api/v1/"
        return super().setUp()

    def tearDown(self) -> None:
        return super().tearDown()

    def create_user(f):
        @wraps(f)
        def wrapper(self, *args, **kwargs):
            user = User()
            user.email = test_email
            user.password = test_pwd
            user.save()
            return f(self, user.id, *args, **kwargs)
        return wrapper

    def test_status(self):
        resp = get(self.url+"status")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), {"status": "OK"})

    def test_users_with_no_header(self):
        resp = get(self.url+"users")
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json(), {"error": "Unauthorized"})

    def test_users_with_invalid_header(self):
        resp = get(self.url+"users", {"Authorization": "Basic invalid_header"})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json(), {"error": "Unauthorized"})

    @create_user
    def test_users_with_valid_header(self, id):
        resp = get(
            self.url+"users",
            headers={"Authorization": f"Basic {token}"})
        resp_json: dict = resp.json()[0]
        self.assertEqual(resp.status_code, 200)
        self.assertIn("created_at", resp_json.keys())
        # self.ass("3685f104-2e86-45ea-8cb1-8edf709b141d", resp_json.get("id"))
        self.assertEqual('bob@hbtn.io', resp_json.get("email"))
        self.assertIsNone(resp_json.get("first_name"))
        self.assertIsNone(resp_json.get("last_name"))


if __name__ == '__main__':
    main(verbosity=2)
