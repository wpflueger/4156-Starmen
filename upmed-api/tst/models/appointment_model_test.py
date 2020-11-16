import unittest
from models.appointment import Appointment
import time


class AppointmentModelTestCase(unittest.TestCase):
    def test_success_build_appointment(self):
        correct_test_appointment = Appointment(
                    id="1",
                    date=int(time.time()),
                    duration=30,
                    doctor=str(100),
                    patient=str(200),
                    subject="Health checkup",
                    notes="Pre existing diabetes and hypertension",
                    videoUrl="https://www.youtube.com/")
        self.assertEqual(correct_test_appointment.duration, 30)
        self.assertEqual(correct_test_appointment.doctor, '100')
        self.assertEqual(correct_test_appointment.patient, '200')
        self.assertEqual(correct_test_appointment.videoUrl, "https://www.youtube.com/")


if __name__ == '__main__':
    unittest.main()
