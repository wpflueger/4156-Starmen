import unittest
from models.day import Day
from models.hours import Hours

class DayTestCase(unittest.TestCase):
    def test_day_model(self):
        normal_office_hours = Day(startTime=540, endTime=1020) #9am to 5pm UTC
        normal_hours = Hours(
            sunday=normal_office_hours,
            monday=normal_office_hours,
            tuesday=normal_office_hours,
            wednesday=normal_office_hours,
            thursday=normal_office_hours,
            friday=normal_office_hours,
            saturday=normal_office_hours
        )
        print (list(normal_hours.monday))
        self.assertEqual(normal_hours.inc(), [540, 1020])


if __name__ == '__main__':
    unittest.main()
