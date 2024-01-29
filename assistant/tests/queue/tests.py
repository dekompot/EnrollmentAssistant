from datetime import datetime

from django.test import TestCase

from assistant.models import Student, EnrollmentPermission, EnrollmentEdition, EnrollmentQueue, FieldOfStudies
from assistant.tests.queue.set_ups import set_up
from assistant.queue.queue import set_early_permissions, add, remove, contains


class TestQueue(TestCase):

    def setUp(self):
        set_up()

    def test_early(self):
        student = Student.objects.get(id='266640')

        set_early_permissions(student.id, True)
        self.assertEquals(EnrollmentPermission.objects.get(student=student).is_permitted_earlier, True)

        set_early_permissions(student.id, False)
        self.assertEquals(EnrollmentPermission.objects.get(student=student).is_permitted_earlier, False)

        set_early_permissions(student.id, True)
        self.assertEquals(EnrollmentPermission.objects.get(student=student).is_permitted_earlier, True)

    def test_add(self):
        student = Student.objects.get(id='266640')
        field_of_study = FieldOfStudies(id='TEST-2024', name='Testowe')
        field_of_study.save()
        enrollment_id = '2024-01-test'
        enrollment_edition = EnrollmentEdition(id=enrollment_id, academic_year='2023/2024',
                                               semester=5, field_of_studies=field_of_study)
        enrollment_edition.save()

        enrollment_queue = EnrollmentQueue(enrollment_edition=enrollment_edition)
        enrollment_queue.save()
        self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 0)
        add(enrollment_edition.id, student.id)
        self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 1)
        self.assertEquals(student.id,
                          EnrollmentPermission.objects.get(queue=enrollment_queue, student=student).student_id)

    def test_remove(self):
        student = Student.objects.get(id='266640')
        field_of_study = FieldOfStudies(id='TEST-2024', name='Testowe')
        field_of_study.save()
        enrollment_id = '2024-01-test'
        enrollment_edition = EnrollmentEdition(id=enrollment_id, academic_year='2023/2024',
                                               semester=5, field_of_studies=field_of_study)
        enrollment_edition.save()

        enrollment_queue = EnrollmentQueue(enrollment_edition=enrollment_edition)
        enrollment_queue.save()

        permission = EnrollmentPermission(queue=enrollment_queue, student=student, date_from=datetime.now(),
                                          date_to=datetime.now())
        permission.save()

        self.assertEquals(permission,EnrollmentPermission.objects.get(queue=enrollment_queue, student=student))
        self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 1)
        remove(enrollment_id, student.id)
        self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 0)

    def test_contains_add_remove(self):
        student = Student.objects.get(id='266640')
        field_of_study = FieldOfStudies(id='TEST-2024', name='Testowe')
        field_of_study.save()
        enrollment_id = '2024-01-test'
        enrollment_edition = EnrollmentEdition(id=enrollment_id, academic_year='2023/2024',
                                               semester=5, field_of_studies=field_of_study)
        enrollment_edition.save()

        enrollment_queue = EnrollmentQueue(enrollment_edition=enrollment_edition)
        enrollment_queue.save()

        permission = EnrollmentPermission(queue=enrollment_queue, student=student, date_from=datetime.now(),
                                          date_to=datetime.now())
        permission.save()

        self.assertEquals(contains(enrollment_queue, student.id), True)
        remove(enrollment_id, student.id)
        self.assertEquals(contains(enrollment_queue, student.id), False)
        add(enrollment_id, student.id)
        self.assertEquals(contains(enrollment_queue, student.id), True)
        # self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 1)
        # remove(enrollment_id, student.id)
        # self.assertEquals(EnrollmentPermission.objects.filter(queue=enrollment_queue).count(), 0)