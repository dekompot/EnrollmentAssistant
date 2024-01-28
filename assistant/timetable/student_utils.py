from datetime import datetime
from typing import List

from assistant.models import FieldOfStudies, Studying, EnrollmentQueue, EnrollmentEdition
from assistant.enrollment.enrollment import get_enrollment_edition
from assistant.models import Student, EnrollmentPermission
from utils.return_codes import PermissionsReturnCodes
from dateutil.parser import parse


def get_field_of_studies(student_id: str) -> List[FieldOfStudies]:
    return [studying.field_of_study for studying in Studying.objects.filter(student__id=student_id)]


def is_student_in_registration_period(student: Student, field_of_studies: str) -> PermissionsReturnCodes:
    enrollment_edition = get_enrollment_edition(field_of_studies)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    enrollment_permissions = EnrollmentPermission.objects.filter(student=student, queue=queue)

    if not enrollment_permissions:
        return PermissionsReturnCodes.NOT_PERMITTED

    return PermissionsReturnCodes.PERMITTED if \
        (enrollment_permissions[0].date_from.timestamp() <= datetime.now().timestamp() < enrollment_permissions[0].date_to.timestamp())\
        else PermissionsReturnCodes.NOT_IN_REGISTRATION_DATE




