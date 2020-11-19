import unittest
from src.util.super_blueprint import SuperBlueprint
from src.api.hcp import hcp_endpoints
from flask import Flask


class TestRegisterBlueprint(unittest.TestCase):
    def test_register_blueprint(self):
        try:
            api_endpoints = SuperBlueprint('appointment', __name__, url_prefix='')
            api_endpoints.register_blueprint(hcp_endpoints, url_prefix='/hcp')
        except Exception as e:
            self.fail(msg='test register blueprint error due to' + str(e))


if __name__ == '__main__':
    unittest.main()
