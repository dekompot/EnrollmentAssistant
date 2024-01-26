import unittest

from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import *
from assistant.mock_data import load_mock_data, generate_mock_students_with_timetables
from assistant.utils.return_codes import EnrollmentReturnCodes
from utils.datetime_utils import as_hour


def setUp():
    load_mock_data()

    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    generate_mock_students_with_timetables(enrollment_edition)

    course_group = CourseGroup(code='TEST00007', name='Test Course Group')
    course = Course(code='TEST00007P', name='Test Course', ECTS=1, course_group=course_group,
                    course_type=CourseType.PRACTICALS)
    group = Group(code='T02-99a', enrollment_edition=enrollment_edition,
                  course=course, week_type=WeekType.EVERY_WEEK, day_of_week=DayOfWeek.MONDAY,
                  start_time=as_hour('9:15'), end_time=as_hour('11:00'), available_seats=1,
                  building='A1', hall='329a')

    student = Student.objects.get(id='266640')
    timetable = Timetable(enrollment_edition=enrollment_edition, student=student)

    timetable.save()
    course_group.save()
    course.save()
    group.save()


class TestRegister(TestCase):

    def setUp(self):
        setUp()

    def test_register_successfully(self):
        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        enrollment = Enrollment(enrollment_edition)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')

        assert enrollment.register(student, group) == EnrollmentReturnCodes.SUCCESS

    def test_register_fail_on_group_already_taken(self):
        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        enrollment = Enrollment(enrollment_edition)

        student_a = Student.objects.get(id='266640')
        student_b = Student.objects.get(id='266661')
        group = Group.objects.get(code__exact='T02-99a')

        assert group.available_seats == 1

        enrollment.register(student_b, group)

        assert enrollment.register(student_a, group) == EnrollmentReturnCodes.GROUP_NOT_AVAILABLE


class TestIsAlreadyRegistered(TestCase):

    def setUp(self):
        setUp()

    def test_is_already_registered(self):
        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        enrollment = Enrollment(enrollment_edition)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')
        timetable = Timetable(enrollment_edition=enrollment_edition, student=student)

        timetable.save()

        assert not enrollment.is_already_registered(timetable, group)
