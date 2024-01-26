from enum import Enum


class EnrollmentReturnCodes(Enum):
    SUCCESS = 0
    GROUP_NOT_AVAILABLE = 1
    STUDENT_ALREADY_IN_COURSE = 2
    GROUP_IS_CONFLICTING = 3
