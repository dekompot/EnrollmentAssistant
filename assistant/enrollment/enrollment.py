from typing import List, Union

from assistant.models import EnrollmentEdition, Student, Group, EnrollmentRecord, Timetable, FieldOfStudies, Studying
from utils.return_codes import EnrollmentReturnCodes


def group_is_conflicting(timetable: Timetable, group: Group):
    return any(group.intervenes_with(record.group)
               for record in timetable.enrollmentrecord_set.all())


def is_group_available(group: Group) -> bool:
    registered_students = EnrollmentRecord.objects.filter(group=group).all()
    return len(registered_students) < group.available_seats


def is_already_registered(timetable: Timetable, group: Group) -> bool:
    course = group.course
    registered = EnrollmentRecord.objects.filter(timetable=timetable, group__course__exact=course)
    return registered.exists()


# With real USOS we'll ask what is the current enrollment edition
def get_enrollment_edition(field_of_studies: Union[str, FieldOfStudies]):
    if type(field_of_studies) is str:
        field_of_studies = FieldOfStudies.objects.get(id=field_of_studies)
    enrollment_editions = EnrollmentEdition.objects.filter(id__exact='summer-2022/2023')
    if not enrollment_editions:
        enrollment_edition = EnrollmentEdition(id='summer-2022/2023', academic_year='2022/2023',
                                           semester=4, field_of_studies__id=field_of_studies.id)
        enrollment_edition.save()
    else:
        enrollment_edition = enrollment_editions[0]
    return enrollment_edition


class Enrollment:

    def __init__(self, field_of_studies):
        self.enrollment_edition = get_enrollment_edition(field_of_studies)

    # This should only communicate with db or also validate?
    def register(self, student: Student, group: Group) -> EnrollmentReturnCodes:
        if not is_group_available(group):
            return EnrollmentReturnCodes.GROUP_NOT_AVAILABLE

        timetable = Timetable.objects.get(enrollment_edition=self.enrollment_edition,
                                          student=student)

        if is_already_registered(timetable, group):
            return EnrollmentReturnCodes.COURSE_ALREADY_TAKEN

        if group_is_conflicting(timetable, group):
            return EnrollmentReturnCodes.GROUP_IS_CONFLICTING

        enrollment_record = EnrollmentRecord(group=group, timetable=timetable)
        enrollment_record.save()
        return EnrollmentReturnCodes.SUCCESS

    def unregister(self, student: Student, group: Group) -> bool:
        timetable = Timetable.objects.get(enrollment_edition=self.enrollment_edition,
                                          student=student)
        enrollment_record = EnrollmentRecord.objects.filter(group=group, timetable=timetable)

        if enrollment_record:
            enrollment_record[0].delete()

        return len(enrollment_record) > 0


