import unittest

from django.test import TestCase

from assistant.controllers.shared import SearchForm, get_filtered_groups
from assistant.enrollment.enrollment import Enrollment
from assistant.test_procedures import load_mock_data
from parsing.parse_json import load_grid_from_json
from assistant.models import *


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


class TestGetFilteredGroups(TestCase):

    def setUp(self):
        load_mock_data()

    def test_get_groups_with_teacher(self):
        form = SearchForm(initial={'teacher': 'Mateusz Mądry'})
        groups = get_filtered_groups(form)
        assert (set(group.code for group in groups)
                == {'K02-75c', 'K02-75d', 'K02-75e', 'K02-75g', 'K02-75f', 'K02-75h', 'K02-75a', 'K02-75b'})

    def test_get_groups_at_day_of_week(self):
        form = SearchForm(initial={'day_of_week': 'Monday'})
        groups = get_filtered_groups(form)
        assert (set(group.code for group in groups)
                == {'K02-75c', 'K02-75d', 'K02-76a', 'K02-77e', 'K05-67a', 'K05-67b', 'K02-81a', 'K02-81b', 'K02-82a'})

    def test_get_groups_at_day_with_teacher(self):
        form = SearchForm(initial={'teacher': 'Mateusz Mądry', 'day_of_week': 'Monday'})
        groups = get_filtered_groups(form)
        assert set(group.code for group in groups) == {'K02-75c', 'K02-75d'}

    def test_get_groups_with_no_results(self):
        form = SearchForm(initial={'group_code': 'K02-73a', 'course_code': 'CBEK00007P'})
        assert not get_filtered_groups(form)

    def test_get_groups_between_hours(self):
        form = SearchForm(initial={'date_from': '9:00', 'date_to': '11:00'})
        groups = get_filtered_groups(form)
        assert set(group.code for group in groups) == {'K02-74a', 'K02-75c', 'K02-75d', 'K02-77d',
                                                       'K02-79c', 'K02-79d', 'K02-81g', 'K02-81h'}