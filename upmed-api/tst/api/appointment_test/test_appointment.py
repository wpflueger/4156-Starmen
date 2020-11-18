import unittest
import requests

from ....src.util.firebase.db import Database
from ....src.models.patient import Patient
from ....src.models.hcp import HCP
from ....src.models.day import Day
from ....src.models.hours import Hours
from ....src.models.enums import Status
from ....src.util.util import Auth
import time
"""
Appoinyment endpoint
Note: run as python3 -m upmed-api.tst.api.appointment_test.appointment_test
"""
appointment_token = ''


def create_dummy_data():
    # Add some dummy patient and hcp
    week = []
    for i in range(0, 7):
        week.append(Day(startTime=540, endTime=1020, ))
    schedule = Hours(
        sunday=week[0],
        monday=week[1],
        tuesday=week[2],
        wednesday=week[3],
        thursday=week[4],
        friday=week[5],
        saturday=week[6])
    dummy_hcp = HCP(
        id="hw2735",
        firstName="Kevin",
        lastName="Wong",
        phone="+19175587800",
        email="hw2735@columbia.edu",
        specialty="Accident and Emergency",
        profilePicture='',
        calendar=[],
        title='Resident',
        patients=[''],
        hours=schedule)

    dummy_patient = Patient(
        id="aoc1989",
        firstName="Alexandria",
        lastName="Ocasio-Cortez",
        phone="0000000000",
        email="aoc@democrat.com",
        dateOfBirth="1989-10-13",
        sex='F',
        profilePicture='',
        height=150,
        weight=60,
        drinker=Status.NEVER,
        smoker=Status.NEVER,
        calendar=[],
        health=[],
        doctors=["hw2735"]
    )
    return dummy_hcp, dummy_patient


class AppointmentApiTestCase(unittest.TestCase):
    auth = Auth()
    pdb = Database()
    hcp_db = pdb.getHCP()
    patient_db = pdb.getPatients()
    appointmentsdb = pdb.getAppointments()
    dummy_hcp, dummy_patient = create_dummy_data()
    hours = []
    time = []
    time.append(dummy_hcp.hours.sunday.startTime)
    time.append(dummy_hcp.hours.sunday.endTime)
    hours.append(str(time))
    time[0] = dummy_hcp.hours.monday.startTime
    time[1] = dummy_hcp.hours.monday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.tuesday.startTime
    time[1] = dummy_hcp.hours.tuesday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.wednesday.startTime
    time[1] = dummy_hcp.hours.wednesday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.thursday.startTime
    time[1] = dummy_hcp.hours.thursday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.friday.startTime
    time[1] = dummy_hcp.hours.friday.endTime
    hours.append(str(time))
    time[0] = dummy_hcp.hours.saturday.startTime
    time[1] = dummy_hcp.hours.saturday.endTime
    hours.append(str(time))

    hcp_db.document(dummy_hcp.id).set({
        "id": dummy_hcp.id,
        "firstName": dummy_hcp.firstName,
        "lastName": dummy_hcp.lastName,
        "phone": dummy_hcp.phone,
        "email": dummy_hcp.email,
        "profilePicture": dummy_hcp.profilePicture,
        "calendar": dummy_hcp.calendar,
        "specialty": dummy_hcp.specialty,
        "title": dummy_hcp.title,
        "hours": hours,
        "patients": dummy_hcp.patients
    })
    patient_db.document(dummy_patient.id).set({
        "id": dummy_patient.id,
        "firstName": dummy_patient.firstName,
        "lastName": dummy_patient.lastName,
        "phone": dummy_patient.phone,
        "email": dummy_patient.email,
        "dateOfBirth": dummy_patient.dateOfBirth,
        "sex": dummy_patient.sex,
        "profilePicture": dummy_patient.profilePicture,
        "height": dummy_patient.height,
        "weight": dummy_patient.weight,
        "drinker": dummy_patient.drinker.value,
        "smoker": dummy_patient.smoker.value,
        "calendar": dummy_patient.calendar,
        "health": dummy_patient.health,
        "doctors": dummy_patient.doctors
    })

    auth_token = auth.encode_auth_token(dummy_hcp.id, "HCP")
    hcp_token = auth_token.decode()

    auth_token = auth.encode_auth_token(dummy_patient.id, "PATIENT")
    patient_token = auth_token.decode()
    appointment_token = ''

    def test_root(self):
        response = requests.post('http://127.0.0.1:8080/appointment/')
        self.assertEqual(200, response.status_code)

    def test_createAppointment(self, hcp_token=hcp_token):
        timpstamp = time.time()
        payload = {
            'token': hcp_token,
            'date': timpstamp,
            'duration': 45,
            'hcpid': 'hw2735',
            'patient': 'aoc1989',
            'subject': 'Follow Up',
            'notes': 'Follow up for her schizophrenia',
            'videoUrl': 'https://www.youtube.com/watch?v=dMTQKFS1tpA'}

        data = payload
        # print(data)

        response = requests.post(
            'http://127.0.0.1:8080/appointment/createAppointment',
            json=data)
        appointment_token = response.json
        # print(appointment_token)
        self.assertEqual(200, response.status_code)

    def test_getCalendar(self, hcp_token=hcp_token):
        payload = {'token': hcp_token
                   }
        response = requests.post(
            'http://127.0.0.1:8080/appointment/getCalendar',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_getByToken(self, hcp_token=hcp_token, id=appointment_token):
        payload = {'token': hcp_token,
                   'id': appointment_token}
        response = requests.post(
            'http://127.0.0.1:8080/appointment/getByToken',
            json=payload)
        self.assertEqual(200, response.status_code)

    def test_delete_appointment(self, hcp_token=hcp_token, id=appointment_token):
        payload = {
            'token': hcp_token,
            'id': appointment_token
        }
        response = requests.post(
            'http://127.0.0.1:8080/appointment/delete_appointment',
            json=payload)
        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()
