from assistant.enrollment.enrollment import get_enrollment_edition
from assistant.models import EnrollmentEdition, Group, EnrollmentRecord


class GroupsHandler:

    def __init__(self, field_of_studies):
        self.enrollment_edition = get_enrollment_edition(field_of_studies)

    def get_taken_seats(self, group_code: str):
        group = Group.objects.filter(code=group_code, enrollment_edition=self.enrollment_edition)

        if not group.exists():
            return -1

        enrollment_records = EnrollmentRecord.objects.filter(group=group[0].code,
                                                             timetable__enrollment_edition=self.enrollment_edition)

        return len(enrollment_records)