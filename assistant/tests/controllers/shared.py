from django.test import TestCase

from assistant.controllers.shared import SearchForm, get_filtered_groups
from assistant.models import Timetable, EnrollmentRecord
from utils.mock_data import load_mock_data


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

