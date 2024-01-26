from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.models import *
from utils.mock_data import load_mock_data, generate_mock_students_with_timetables
from utils.return_codes import EnrollmentReturnCodes
from utils.datetime_utils import as_hour

def set_up():
    load_mock_data()

    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    generate_mock_students_with_timetables(enrollment_edition)

    # Generate some mock objects
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