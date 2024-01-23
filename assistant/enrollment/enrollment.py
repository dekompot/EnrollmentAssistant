from assistant.models import EnrollmentEdition, Student, Group, EnrollmentRecord, Timetable
from assistant.utils.return_codes import ReturnCode


class Enrollment:

    def __init__(self, enrollment_edition: EnrollmentEdition):
        self.enrollment_edition = enrollment_edition

    # This should only communicate with db or also validate?
    def register(self, student: Student, group: Group) -> ReturnCode:
        if not self.is_group_available(group):
            return ReturnCode.GROUP_NOT_AVAILABLE

        timetable = Timetable.objects.get(enrollment_edition=self.enrollment_edition,
                                          student=student)
        '''
        if self.is_already_registered(timetable, group):
            return ReturnCode.STUDENT_ALREADY_IN_COURSE
        '''

        if not self.can_be_regsitered(timetable, group):
            return ReturnCode.GROUP_IS_CONFLICTING

        enrollment_record = EnrollmentRecord(group=group, timetable=timetable)
        enrollment_record.save()
        return ReturnCode.SUCCESS

    def can_be_regsitered(self, timetable: Timetable, group: Group):
        # mock implementation
        return True

    def is_group_available(self, group: Group) -> bool:
        registered_students = EnrollmentRecord.objects.filter(group=group).all()
        return len(registered_students) < group.available_seats


    def is_already_registered(self, timetable: Timetable, group: Group) -> bool:
        course = group.course
        registered = EnrollmentRecord.objects.filter(timetable=timetable, group__course__exact=course)
        return registered.exists()