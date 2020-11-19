import unittest

from ...src.util.super_blueprint import SuperBlueprint
from ...src.api.appointment import appointment_endpoints


class TestUtil(unittest.TestCase):
    superblueprint = SuperBlueprint('appointment', __name__, url_prefix='')

    def test_superblueprint(self):
        try:
            self.superblueprint.register_blueprint(appointment_endpoints, url_prefix='/hcp')
        except Exception as e:
            self.fail("test superblueprint raised exception: " + str(e))


if __name__ == '__main__':
    unittest.main()
