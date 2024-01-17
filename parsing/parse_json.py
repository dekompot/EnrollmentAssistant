import json

from assistant.models import Course, CourseGroup, EnrollmentEdition, FieldOfStudies
from parsing.parse_elements import group_factory, map_form_of_classes


def load_from_file(file: str):
    with open(file, encoding='utf-8') as f:
        return json.load(f)


def load_from_json(file: str, save_to_db: bool = False):
    courses = []

    field_of_studies = FieldOfStudies(id='CBE-2022', name='Cyberbezpieczenstwo')
    enrollment_edition = EnrollmentEdition(id='1', academic_year='2022/2023', semester=3)

    if save_to_db:
        field_of_studies.save()
        enrollment_edition.save()

    loaded_json = load_from_file(file)
    print(json.dumps(loaded_json, indent=4))

    for loaded_course in loaded_json['courses']:
        course_group = CourseGroup(name=loaded_course['name'], number_of_choices=1)
        course_type = map_form_of_classes(loaded_course['code'])
        course = Course(code=loaded_course['code'], name=loaded_course['name'], ECTS=0,
                        course_group=course_group, course_type=course_type)
        courses.append(course)
        course_groups = [group_factory(code=group['code'], date_and_place=group['date_and_place'],
                                       enrollment_edition=enrollment_edition, course=course)
                         for group in loaded_course['groups']]

        if save_to_db:
            course_group.save()
            course.save()
            for group in course_groups:
                group.save()

    return courses

if __name__ == '__main__':
    load_from_json('assistant/data/plan_kacpra.json')