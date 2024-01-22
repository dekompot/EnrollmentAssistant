from assistant.models import EnrollmentEdition, FieldOfStudies, Student
from parsing.parse_json import load_grid_from_json

def load_mock_data():

    field_of_study = FieldOfStudies(id='CBE-2021-inz', name='Cyberbezpieczenstwo')
    student = Student(id='266640', name='Kacper Bartocha', average=4.5)

    enrollment_edition = EnrollmentEdition(id='summer-2022/2023', academic_year='2022/2023',
                                           semester=4, field_of_studies=field_of_study)

    field_of_study.save()
    student.save()
    enrollment_edition.save()

    load_grid_from_json(enrollment_edition_id=enrollment_edition.id,
                        file='assistant/data/plan_kacpra.json')