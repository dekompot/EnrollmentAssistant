from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import *
from enrollment.set_ups import *
from utils.mock_data import load_mock_data, generate_mock_students
from utils.return_codes import EnrollmentReturnCodes
from utils.datetime_utils import as_hour


# One test per one method - one testing method for one possible case
class TestRegister(TestCase):

    def setUp(self):
        set_up()

    def test_register_successfully(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')

        self.assertEquals(enrollment.register(student, group), EnrollmentReturnCodes.SUCCESS)

    def test_register_fail_on_group_not_available(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student_a = Student.objects.get(id='266640')
        student_b = Student.objects.get(id='266661')
        group = Group.objects.get(code__exact='T02-99a')

        self.assertEquals(group.available_seats, 1)

        enrollment.register(student_b, group)

        self.assertEquals(enrollment.register(student_a, group), EnrollmentReturnCodes.GROUP_NOT_AVAILABLE)

    def test_register_fail_on_conflicting_groups(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student = Student.objects.get(id='266640')
        group_1 = Group.objects.get(code__exact='K02-75h')
        group_2 = Group.objects.get(code__exact='K02-79g')

        self.assertTrue(group_1.intervenes_with(group_2))

        self.assertEquals(enrollment.register(student, group_1), EnrollmentReturnCodes.SUCCESS)

        self.assertEquals(enrollment.register(student, group_2), EnrollmentReturnCodes.GROUP_IS_CONFLICTING)

    def test_register_fail_on_course_already_taken(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student = Student.objects.get(id='266640')
        [group_1, group_2, *_] = Group.objects.filter(course__code='CBEK00027L')

        self.assertEquals(enrollment.register(student, group_1), EnrollmentReturnCodes.SUCCESS)

        self.assertEquals(enrollment.register(student, group_2), EnrollmentReturnCodes.COURSE_ALREADY_TAKEN)


class TestUnregister(TestCase):
    def setUp(self):
        set_up()

    def test_unregister_successfully(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')

        enrollment.register(student, group)
        self.assertTrue(enrollment.unregister(student, group))

    def test_unregister_failure(self):
        enrollment = Enrollment(FIELD_OF_STUDIES)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')

        self.assertFalse(enrollment.unregister(student, group))