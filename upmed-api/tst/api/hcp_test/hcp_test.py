import unittest
from unittest.mock import MagicMock, Mock, patch
import json
from sys import path
from os.path import join, dirname
from src.api.patient.patient_helper import *
from src.api.hcp.hcp_helper import *
from src import Database, Patient, Appointment, HCP, Day, Hours, Status, Auth, hcp, Twilio  # noqa
from tst.mock_helpers import MockHCP, MockAppointment, MockPatient  # noqa

path.append(join(dirname(__file__), '../../..'))

"""
HCP Endpoint Tests
"""

auth = Auth()
twilio = Twilio()

# Set up dummy database and dummy objects
default_value_1 = 1
default_value_2 = 2
default_value_3 = 3

appointment_token = 'aoc1989,hw2735,1605841671.366644'
mockpatient = MockPatient()
mockhcp = MockHCP()
mockappointment = MockAppointment()

unittest.TestLoader.sortTestMethodsUsing = None
hcp_token = ''

twilio_set_func = Mock()
twilio_set_func.connect.messages.create = MagicMock(return_value=default_value_1)


class HCPTestCase(unittest.TestCase):
    # Mock statements for template use
    # db = Mock()
    # set_func = Mock()
    # set_func.to_dict = MagicMock(return_value=default_value_1)
    # set_func.set = MagicMock(return_value=default_value_1)
    # set_func.update = MagicMock(return_value=default_value_1)
    # set_func.get = MagicMock(return_value=default_value_1)
    # set_func.stream = MagicMock(return_value=default_value_2)
    # set_func.delete = MagicMock(return_value=default_value_3)
    # db.stream = MagicMock(return_value=default_value_2)
    # db.document = MagicMock(return_value=set_func)

    def test_signup_test(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=default_value_1)
        set_func.set = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)
        week = []
        for i in range(0, 7):
            week.append(Day(startTime=540, endTime=1020))
        schedule = Hours(
            sunday=week[0],
            monday=week[1],
            tuesday=week[2],
            wednesday=week[3],
            thursday=week[4],
            friday=week[5],
            saturday=week[6])

        payload = {'id': "ap0000",
                   'firstName': "Athena",
                   'lastName': "Pang",
                   'phone': '"9175587800"',
                   'email': "ap0000@columbia.edu",
                   'specialty': "Accident and Emergency",
                   'hours': {
                       "sunday": {
                           "startTime": schedule.sunday.startTime,
                           "endTime": schedule.sunday.endTime
                       },
                       "monday": {
                           "startTime": schedule.monday.startTime,
                           "endTime": schedule.monday.endTime
                       },
                       "tuesday": {
                           "startTime": schedule.tuesday.startTime,
                           "endTime": schedule.tuesday.endTime
                       },
                       "wednesday": {
                           "startTime": schedule.wednesday.startTime,
                           "endTime": schedule.wednesday.endTime
                       },
                       "thursday": {
                           "startTime": schedule.thursday.startTime,
                           "endTime": schedule.thursday.endTime
                       },
                       "friday": {
                           "startTime": schedule.friday.startTime,
                           "endTime": schedule.friday.endTime
                       },
                       "saturday": {
                           "startTime": schedule.saturday.startTime,
                           "endTime": schedule.saturday.endTime
                       }
                   }
                   }
        res = hcp_signup(db, mockhcp.hcp, mockhcp.hcp.hours, 'JON')
        self.assertNotEqual(res, 0)
        # self.assertEqual(res, 1)

    def test_login_test(self):
        func = Mock()
        func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        func.get = MagicMock(return_value=mockhcp.hcp)
        db_2 = Mock()
        db_2.document = MagicMock(return_value=func)

        res = hcp_login(db_2, mockhcp.hcp.id, mockhcp.hcp.email)
        self.assertNotEqual(res, 0)

    def test_set_record(self):
        db = Mock()
        set_func = Mock()
        set_func.set = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)

        res = hcp_set_record(db, mockpatient.patient)
        self.assertEqual(res, default_value_1)

    @patch("api.hcp_helper.Twilio.connect", return_value=twilio_set_func)
    def test_notify_test(self, mock):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)

        adb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockappointment.appointment.to_dict())
        set_func2.get = MagicMock(return_value=mockappointment.appointment)
        adb.document = MagicMock(return_value=set_func2)

        res = hcp_notify(adb, db, mockappointment.appointment.id)
        print(res)
        self.assertTrue(mock.called, "twilio not being called")
        self.assertTrue(res['Success'], 0)

    def test_remove_test(self):
        db = Mock()
        set_func = Mock()
        set_func.delete = MagicMock(return_value=default_value_3)
        db.document = MagicMock(return_value=set_func)
        res = hcp_delete(db, mockhcp.hcp.id)
        self.assertEqual(res, 3)

    def test_getByToken(self):
        set_func = Mock()
        db = Mock()
        set_func.get = MagicMock(return_value=mockhcp.hcp)
        db.document = MagicMock(return_value=set_func)

        res = hcp_get_by_token(db, mockhcp.hcp.id)
        self.assertTrue(isinstance(res, HCP))

    @patch("api.hcp_helper.Twilio.connect", return_value=twilio_set_func)
    def test_test_number(self, mock):
        adb = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockappointment.appointment.to_dict())
        set_func.get = MagicMock(return_value=mockappointment.appointment)
        adb.document = MagicMock(return_value=set_func)

        pdb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func2.get = MagicMock(return_value=mockpatient.patient)
        pdb.document = MagicMock(return_value=set_func2)

        res = hcp_test_number(adb, pdb, mockappointment.appointment.id)
        self.assertTrue(mock.called, "twilio not being called")
        self.assertTrue(res['Success'], 0)

    def test_edit_profile(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockhcp.hcp)
        db.document = MagicMock(return_value=set_func)
        payload = {
            'id': 'hw2735',
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'specialty': 'family medicine',
            'title': 'consultant',
            'profilePicture': 'dummy profile pic',
            'hours': mockhcp.hcp.hours.to_dict()
        }
        res = hcp.hcp_edit_profile(db, mockhcp.hcp.id, payload)
        print("the response is: =====================")
        print(res)

        self.assertTrue(res['Success'])
        payload = {
            'id': 'pyy1010',
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'specialty': 'family medicine',
            'title': 'consultant',
            'profilePicture': 'dummy profile pic',
            'hours': mockhcp.hcp.hours.to_dict()
        }
        res = hcp.hcp_edit_profile(db, mockhcp.hcp.id, payload)
        print("the response is: =====================")
        print(res)
        self.assertFalse(res['Success'])

    def test_health_event(self):
        db = Mock()
        set_func = Mock()
        set_func.set = MagicMock(return_value=default_value_1)
        set_func.get = MagicMock(return_value=mockpatient.patient)
        db.document = MagicMock(return_value=set_func)
        payload = {
            'firstName': 'athena',
            'lastName': 'pang',
            'phone': '9175587880',
            'email': 'fake email address',
            'height': '156',
            'weight': '50',
            'drinker': 0,
            'smoker': 0,
            'calendar': ['aoc1989,hw2735,1605841671.366644'],
            'doctors': ["hw2735", "fyy1010"],
            'health': mockpatient.patient.health
        }
        res = hcp_set_health_events(db, mockpatient.patient.id, payload)
        self.assertIsInstance(res, Patient)

    def test_get_all(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        db.stream = MagicMock(return_value=[mockhcp.hcp, mockhcp.hcp])

        res = hcp_get_all(db)
        self.assertEqual(res[0]["id"], mockhcp.hcp.id)
        self.assertEqual(res[1]["id"], mockhcp.hcp.id)

    def test_get_patients(self):
        db = Mock()
        set_func = Mock()
        set_func.to_dict = MagicMock(return_value=mockhcp.hcp.to_dict())
        set_func.get = MagicMock(return_value=mockhcp.hcp)
        db.document = MagicMock(return_value=set_func)

        pdb = Mock()
        set_func2 = Mock()
        set_func2.to_dict = MagicMock(return_value=mockpatient.patient.to_dict())
        set_func2.get = MagicMock(return_value=mockpatient.patient)
        pdb.document = MagicMock(return_value=set_func2)

        res = hcp_get_patients(db, pdb, mockhcp.hcp.id)
        self.assertEqual(res['aoc1989']['id'], 'aoc1989')

    def test_set_profile_picture(self):
        db = Mock()
        set_func = Mock()
        set_func.update = MagicMock(return_value=default_value_1)
        db.document = MagicMock(return_value=set_func)

        res = hcp_set_profile_picture(
            db, mockhcp.hcp.id, mockhcp.hcp.profilePicture)
        self.assertEqual(res, mockhcp.hcp.profilePicture)


if __name__ == '__main__':
    unittest.main()
