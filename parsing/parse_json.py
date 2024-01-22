import json

from assistant.models import Course, CourseGroup, EnrollmentEdition, FieldOfStudies, Teacher, Lecturing
from parsing.parse_elements import group_factory, map_form_of_classes, parse_teacher


def load_from_file(file: str):
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def load_grid_from_json(enrollment_edition_id: str, file: str, save_to_db: bool = False):
    courses = []
    teachers = []

    enrollment_edition = EnrollmentEdition.objects.get(id=enrollment_edition_id)

    loaded_json = load_from_file(file)
    print(json.dumps(loaded_json, indent=4))

    for loaded_course in loaded_json['courses']:
        course_group = CourseGroup(code=loaded_course['code'], name=loaded_course['name'])
        course_type = map_form_of_classes(loaded_course['code'])

        teachers = [parse_teacher(group['lecturer']) for group in loaded_course['groups']]

        # lecturing = Lecturing(teacher_id=teacher.id, course_id=course_group)

        course = Course(code=loaded_course['code'], name=loaded_course['name'], ECTS=0,
                        course_group=course_group, course_type=course_type)
        courses.append(course)
        course_groups = [group_factory(code=group['code'], date_and_place=group['date_and_place'],
                                       enrollment_edition=enrollment_edition, course=course)
                         for group in loaded_course['groups']]

        if save_to_db:
            # lecturing.save()
            course_group.save()
            course.save()
            for group in course_groups:
                group.save()

            for teacher in teachers:
                if not Teacher.objects.filter(name=teacher.name, title=teacher.title):
                    teacher.id = Teacher.objects.last().id + 1
                    teacher.save()

    return courses
