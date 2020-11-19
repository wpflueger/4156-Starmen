import unittest
from src.util.util import Auth, Twilio


class TestUtil(unittest.TestCase):
    def test_encode_authtoken(self):
        test_id = 'aoc'
        test_utype = 'HCP'
        auth_object = Auth()
        auth_token = auth_object.encode_auth_token(test_id, test_utype)
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_authtoken(self):
        try:
            test_id = 'aoc'
            test_utype = 'HCP'
            auth_object = Auth()
            auth_token = auth_object.encode_auth_token(test_id, test_utype)
            test_id, test_utype = auth_object.decode_auth_token(auth_token)
            self.assertEqual(test_utype, 'HCP')
        except Exception as e:
            self.fail(msg='test decode authtoken error due to' + str(e))

    def test_twilio(self):
        try:
            twilio_object = Twilio()
            twilio_object.connect()
        except Exception as e:
            self.fail(msg='test twilio error due to' + str(e))


if __name__ == '__main__':
    unittest.main()
