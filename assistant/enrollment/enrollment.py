from assistant.models import EnrollmentEdition, Student, Group, EnrollmentRecord, Timetable
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


class Enrollment:

    def __init__(self, enrollment_edition: EnrollmentEdition):
        self.enrollment_edition = enrollment_edition

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

