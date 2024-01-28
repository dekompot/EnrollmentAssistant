from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import Student
from enrollment.set_ups import FIELD_OF_STUDIES, set_up
from utils.mock_data import load_mock_data
from assistant.timetable.student_utils import is_student_in_registration_period


class TestIsStudentInRegistrationPeriod(TestCase):

    def setUp(self) -> None:
        set_up()

    def test_student_is_permitted(self):
        student = Student.objects.get(id='266640')
        self.assis_student_in_registration_period(student, FIELD_OF_STUDIES)

    def test_student_is_not_permitted(self):
        student = Student.objects.get(id='266662')
        return is_student_in_registration_period(student, FIELD_OF_STUDIES)