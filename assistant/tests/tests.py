'''
Write here tests for debugging purposes
'''
from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from parsing.parse_json import load_grid_from_json
from assistant.models import *


class TestDayOfWeek(TestCase):

    def test_days_of_week_comparison(self):
        print(DayOfWeek.MONDAY)


class TestLoadingFromJson(TestCase):

    def test_load_grid_from_json(self):

        field_of_study = FieldOfStudies(id='CBE-2021-inz', name='Cyberbezpieczenstwo')
        student = Student(id='266640', name='Kacper Bartocha', average=4.5)

        enrollment_edition = EnrollmentEdition(id='summer-2022/2023', academic_year='2022/2023',
                                               semester=4, field_of_studies=field_of_study)

        field_of_study.save()
        student.save()
        enrollment_edition.save()

        load_grid_from_json(enrollment_edition_id=enrollment_edition.id,
                            file='assistant/data/plan_kacpra.json')

    def test_sign_up_student(self):

        field_of_study = FieldOfStudies(id='CBE-2021-inz', name='Cyberbezpieczenstwo')
        student = Student(id='266640', name='Kacper Bartocha', average=4.5)

        enrollment_edition = EnrollmentEdition(id='summer-2022/2023', academic_year='2022/2023',
                                               semester=4, field_of_studies=field_of_study)

        field_of_study.save()
        student.save()
        enrollment_edition.save()

        load_grid_from_json(enrollment_edition_id=enrollment_edition.id,
                            file='assistant/data/plan_kacpra.json')

        timetable = Timetable(enrollment_edition=enrollment_edition, student=student)
        timetable.save()

        group_ids_to_enroll = ['K05-67j', 'K02-82a', 'K02-75d', 'K02-73d']
        groups = Group.objects.filter(code__in=group_ids_to_enroll).all()

        enrollment = Enrollment(enrollment_edition=enrollment_edition)

        for group in groups:
            enrollment.register(student, group)