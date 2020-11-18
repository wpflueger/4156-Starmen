import unittest

from ...src.util.util import Auth
from ...src.util.util import Twilio


class TestUtil(unittest.TestCase):
    token = None
    auth_object = Auth()

    def test_encode_auth_token(self):
        user_id = "dummy"
        user_type = "HCP"
        self.token = self.auth_object.encode_auth_token(user_id=user_id, type=user_type)
        self.assertTrue(isinstance(self.token, str))

    def test_decode_auth_token(self):
        user_id, user_type = self.auth_object.decode_auth_token(self.token)
        self.assertEqual(user_id, "dummy")
        self.assertEqual(user_type, "HCP")

    def test_twilio(self):
        twilio_object = Twilio()
        try:
            client = twilio_object.connect()
        except Exception as e:
            self.fail("test_twilio raised exception: " + str(e))


if __name__ == '__main__':
    unittest.main()
