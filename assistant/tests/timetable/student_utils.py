from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import Student
from enrollment.set_ups import FIELD_OF_STUDIES, set_up
from utils.mock_data import load_mock_data
from assistant.timetable.student_utils import is_student_in_registration_period
from utils.return_codes import PermissionsReturnCodes


class TestIsStudentInRegistrationPeriod(TestCase):

    def setUp(self) -> None:
        set_up()

    def test_student_is_permitted(self):
        student = Student.objects.get(id='266640')
        self.assertEquals(is_student_in_registration_period(student, FIELD_OF_STUDIES),
                          PermissionsReturnCodes.PERMITTED)

    def test_student_is_out_of_registration_date(self):
        student = Student.objects.get(id='266662')
        self.assertEquals(is_student_in_registration_period(student, FIELD_OF_STUDIES),
                          PermissionsReturnCodes.NOT_IN_REGISTRATION_DATE)

    def test_student_is_not_permitted(self):
        student = Student.objects.get(id='266664')
        self.assertEquals(is_student_in_registration_period(student, FIELD_OF_STUDIES),
                          PermissionsReturnCodes.NOT_PERMITTED)