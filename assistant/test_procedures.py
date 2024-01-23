from assistant.enrollment.enrollment import Enrollment
from assistant.models import EnrollmentEdition, FieldOfStudies, Student, Timetable, Group
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

def load_sign_up_mock():
    student = Student.objects.get(id='266640')
    enrollment_edition = EnrollmentEdition.objects.get(id='summer-2022/2023')
    timetable = Timetable(enrollment_edition=enrollment_edition, student=student)
    timetable.save()

    group_ids_to_enroll = ['K05-67j', 'K02-82a', 'K02-75d', 'K02-73d']
    groups = Group.objects.filter(code__in=group_ids_to_enroll).all()

    enrollment = Enrollment(enrollment_edition=enrollment_edition)

    for group in groups:
        enrollment.register(student, group)

