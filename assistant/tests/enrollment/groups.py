from django.test import TestCase

from assistant.enrollment.enrollment import Enrollment
from assistant.enrollment.groupshandler import GroupsHandler
from assistant.models import Student, Group
from enrollment.set_ups import set_up


class TestTakenSeats(TestCase):

    def setUp(self):
        set_up()

    def test_taken_seats_for_empty_group(self):

        groups_handler = GroupsHandler('CBE-2021-inz')
        self.assertEquals(groups_handler.get_taken_seats('K02-73a'), 0)

    def test_taken_seats_for_partially_filled_group(self):
        enrollment = Enrollment('CBE-2021-inz')
        student = Student.objects.get(id='266640')

        group = Group.objects.get(code='K02-73a')

        enrollment.register(student, group)

        groups_handler = GroupsHandler('CBE-2021-inz')
        self.assertEquals(groups_handler.get_taken_seats('K02-73a'), 1)