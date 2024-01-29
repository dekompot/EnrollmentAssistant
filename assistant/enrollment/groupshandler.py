from assistant.enrollment.enrollment import get_enrollment_edition
from assistant.models import EnrollmentEdition, Group, EnrollmentRecord


class GroupsHandler:
    """
    Manages information related to groups and enrollment records for a specific enrollment edition.

    Attributes:
    - enrollment_edition (EnrollmentEdition): The enrollment edition associated with the handler.

    Methods:
    - get_taken_seats(group_code: str) -> int: Retrieves the number of taken seats for a specific group.

    """
    def __init__(self, field_of_studies):
        self.enrollment_edition = get_enrollment_edition(field_of_studies)

    def get_taken_seats(self, group_code: str):
        group = Group.objects.filter(code=group_code, enrollment_edition=self.enrollment_edition)

        if not group.exists():
            return -1

        enrollment_records = EnrollmentRecord.objects.filter(group=group[0].code,
                                                             timetable__enrollment_edition=self.enrollment_edition)

        return len(enrollment_records)