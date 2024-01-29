
from assistant.models import *
from utils.mock_data import load_mock_data, generate_mock_students

FIELD_OF_STUDIES = 'CBE-2021-inz'


def set_up():
    load_mock_data()

    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    generate_mock_students(enrollment_edition)
