import json

from assistant.models import Course, CourseGroup, EnrollmentEdition, FieldOfStudies, Teacher, Lecturing
from parsing.parse_elements import group_factory, map_form_of_classes, parse_teacher, create_teacher


def load_from_file(file: str):
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def load_grid_from_json(enrollment_edition_id: str, file: str):
    courses = []

    enrollment_edition = EnrollmentEdition.objects.get(id=enrollment_edition_id)

    loaded_json = load_from_file(file)
    print(json.dumps(loaded_json, indent=4))

    for loaded_course in loaded_json['courses']:
        course_group = CourseGroup(code=loaded_course['code'], name=loaded_course['name'])
        course_type = map_form_of_classes(loaded_course['code'])

        teachers = [create_teacher(group['lecturer']) for group in loaded_course['groups']]

        course = Course(code=loaded_course['code'], name=loaded_course['name'], ECTS=0,
                        course_group=course_group, course_type=course_type)

        courses.append(course)

        course_groups = [group_factory(code=group['code'], date_and_place=group['date_and_place'],
                                       enrollment_edition=enrollment_edition, course=course)
                         for group in loaded_course['groups']]

        lecturings = [Lecturing(teacher_id=teacher, group_code=group)
                      for (teacher, group) in zip(teachers, course_groups)]

        course_group.save()
        course.save()

        for group in course_groups:
            group.save()

        for lecturing in lecturings:
            lecturing.save()

    # return courses
