from typing import Tuple
from datetime import datetime
import re
from assistant.models import DayOfWeek, WeekType, CourseGroup, Teacher, Group, Course, CourseType, EnrollmentEdition
from utils.datetime_utils import day_from_polish_abbr, as_hour

# W tym module moze bedziemy dawac jakies funkcje do parsowania

PLACE_AND_DATE_REGEX = re.compile("(?P<day_of_week>\w{2})(?P<type_of_week>[TPN+12/]*) "
                                "(?P<hour_start>\d{2}:\d{2})-(?P<hour_end>\d{2}:\d{2}), "
                                  "bud. (?P<building>[-\w]+), sala (?P<hall>\w+)")

TEACHER_REGEX = re.compile("(?P<title>(Prof. dr hab.|Prof. dr hab. inż.|Mgr inż.|Mgr|Dr hab. inż.|Dr hab.|Dr inż.|Dr)) "
                           "(?P<name>.+)")

MAP_POLISH_FORM = {'Zajęcia laboratoryjne': CourseType.LABORATORY,
                   'Ćwiczenia': CourseType.PRACTICALS,
                   'Wykład': CourseType.LECTURE,
                   'Seminarium': CourseType.SEMINARY,
                   'Projekt': CourseType.PROJECT}

MAP_POLISH_ABBR_FORM = {
                    'L': CourseType.LABORATORY,
                   'C': CourseType.PRACTICALS,
                   'W': CourseType.LECTURE,
                   'S': CourseType.SEMINARY,
                   'P': CourseType.PROJECT
}


def parse_date_and_place(date_and_place: str) -> Tuple[DayOfWeek, WeekType, datetime, datetime, str, str]:
    match = PLACE_AND_DATE_REGEX.match(date_and_place)
    day_of_week = day_from_polish_abbr(match.group("day_of_week"))
    type_of_week = WeekType.EVERY_WEEK if len(match.group("type_of_week")) == 0 \
        else WeekType.EVEN_WEEK if match.group("type_of_week").startswith("/TP") else WeekType.ODD_WEEK
    start_time = as_hour(match.group("hour_start"))
    end_time = as_hour(match.group("hour_end"))
    return day_of_week, type_of_week, start_time, end_time, match.group("building"), match.group("hall")


def map_form_of_classes(polish_form: str) -> CourseType:
    return MAP_POLISH_ABBR_FORM[polish_form[-1]]


def parse_teacher(teacher: str) -> Teacher:
    matched_elements = TEACHER_REGEX.match(teacher)
    return Teacher(name=matched_elements.group("name"), title=matched_elements.group("title"))


def group_factory(code: str, date_and_place: str, enrollment_edition: EnrollmentEdition, course: Course):
    day_of_week, type_of_week, start_time, end_time, building, hall = parse_date_and_place(date_and_place)

    return Group(code=code, enrollment_edition=enrollment_edition, course=course, day_of_week=day_of_week, week_type=type_of_week,
                 start_time=start_time, end_time=end_time, building=building, hall=hall)