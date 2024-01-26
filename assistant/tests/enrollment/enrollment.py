import unittest

from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import *
from assistant.test_procedures import load_mock_data
from utils.datetime_utils import as_hour


class TestRegister(TestCase):

    def setUp(self):
        load_mock_data()

        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        course_group = CourseGroup(code='TEST00007', name='Test Course Group')
        course = Course(code='TEST00007P', name='Test Course', ECTS=1, course_group=course_group,
                        course_type=CourseType.PRACTICALS)
        group = Group(code='T02-99a', enrollment_edition=enrollment_edition,
                      course=course, week_type=WeekType.EVERY_WEEK, day_of_week=DayOfWeek.MONDAY,
                      start_time=as_hour('9:15'), end_time=as_hour('11:00'), available_seats=1,
                      building='A1', hall='329a')

        course_group.save()
        course.save()
        group.save()


class TestIsAlreadyRegistered(TestCase):

    def setUp(self):
        load_mock_data()

        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        course_group = CourseGroup(code='TEST00007', name='Test Course Group')
        course = Course(code='TEST00007P', name='Test Course', ECTS=1, course_group=course_group,
                        course_type=CourseType.PRACTICALS)
        group = Group(code='T02-99a', enrollment_edition=enrollment_edition,
                      course=course, week_type=WeekType.EVERY_WEEK, day_of_week=DayOfWeek.MONDAY,
                      start_time=as_hour('9:15'), end_time=as_hour('11:00'), available_seats=1,
                      building='A1', hall='329a')

        course_group.save()
        course.save()
        group.save()

    def test_is_already_registered(self):
        enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
        enrollment = Enrollment(enrollment_edition)

        student = Student.objects.get(id='266640')
        group = Group.objects.get(code__exact='T02-99a')
        timetable = Timetable(enrollment_edition=enrollment_edition, student=student)

        timetable.save()

        assert not enrollment.is_already_registered(timetable, group)