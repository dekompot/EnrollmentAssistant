import datetime
from typing import List, Union

from django.forms import forms, DateTimeField, DateTimeInput
from django.forms import ChoiceField, Select
from django.http import Http404
from django.shortcuts import render

from assistant.enrollment.groupshandler import GroupsHandler
from assistant.models import (DayOfWeek, Course, Lecturing, Student, Timetable,
                              EnrollmentRecord, Group, Teacher)


def timetable(request, student_id):
    """
    Renders the timetable view for a specific student.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - render: The rendered timetable view.
    """
    try:
        student_timetable = Timetable.objects.get(student_id=student_id)
    except Timetable.DoesNotExist:
        raise Http404("Student timetable does not exist")

    enrollment_records = EnrollmentRecord.objects.filter(timetable=student_timetable).all()
    all_groups = [enr.group for enr in enrollment_records]
    groups = [sorted(list(filter(lambda group: group.day_of_week == day, all_groups)), key=lambda group: group.start_time) for day in DayOfWeek]

    context = {
        'groups': groups,
        'student_id': student_id
    }

    return render(request, 'assistant/timetable.html', context)


def group_details(request, group_code: str):
    """
    Renders the group details view for a specific group.

    Parameters:
    - request: The HTTP request object.
    - group_code (str): The code of the group.

    Returns:
    - render: The rendered group details view.
    """
    try:
        group = Group.objects.get(code__exact=group_code)
    except Group.DoesNotExist:
        raise Http404("Group does not exist")

    groups_handler = GroupsHandler('CBE-2021-inz')
    taken_seats = groups_handler.get_taken_seats(group_code)

    context = {
        'group_info': {'code': group.code, 'course': group.course.name,
                       'taken': taken_seats, 'available': group.available_seats,
                       'day_of_week': group.day_of_week}
    }

    return render(request, 'assistant/group_details.html', context)


def get_groups():
    """
    Retrieves a list of groups for form choices.

    Returns:
    - List[Tuple[str, str]]: List of tuples representing group choices.
    """
    groups = Group.objects.all()
    return [('', '')] + [(group.code, group.code) for group in groups]


def get_courses():
    """
       Retrieves a list of courses for form choices.

       Returns:
       - List[Tuple[str, str]]: List of tuples representing course choices.
       """
    courses = Course.objects.all()
    return [('', '')] + [(course.code, course.code) for course in courses]


def get_teachers():
    """
        Retrieves a list of teachers for form choices.

        Returns:
        - List[Tuple[str, str]]: List of tuples representing teacher choices.
        """
    teachers = Teacher.objects.all()
    return [('', '')] + [(teacher.name, teacher.name) for teacher in teachers]


def get_days_of_week():
    """
        Retrieves a list of days of the week for form choices.

        Returns:
        - List[Tuple[str, str]]: List of tuples representing day of the week choices.
        """
    days_of_week = DayOfWeek.choices
    return [('', '')] + days_of_week


class SearchForm(forms.Form):
    """
    Form for searching groups based on specified criteria.
    All entries are optional to fill in. Provided default
    values return all groups for the given enrollment edition

    Attributes:
    - group_code (ChoiceField): The choice field for selecting group codes.
    - course_code (ChoiceField): The choice field for selecting course codes.
    - teacher (ChoiceField): The choice field for selecting teachers.
    - date_from (DateTimeField): The date and time field for specifying the starting date and time.
    - date_to (DateTimeField): The date and time field for specifying the ending date and time.
    - day_of_week (ChoiceField): The choice field for selecting days of the week.

    Methods:
    - is_valid(): Checks if the form is valid and validates date_from and date_to.

    """
    group_code = ChoiceField(widget=Select, choices=get_groups, required=False)
    course_code = ChoiceField(widget=Select, choices=get_courses, required=False)
    teacher = ChoiceField(widget=Select, choices=get_teachers, required=False)
    date_from = DateTimeField(widget=DateTimeInput, input_formats=['%H:%M', ], initial='00:00')
    date_to = DateTimeField(widget=DateTimeInput, input_formats=['%H:%M', ], initial='23:59')
    day_of_week = ChoiceField(widget=Select, choices=get_days_of_week, required=False)

    def is_valid(self):
        """
        Overrides the default is_valid method to validate date_from and date_to.

        Returns:
        - bool: True if the form is valid, False otherwise.

        """
        is_valid = super().is_valid()

        if not is_valid:
            return False

        date_from = datetime.datetime.strptime(self['date_from'].value(), '%H:%M')
        date_to = datetime.datetime.strptime(self['date_to'].value(), '%H:%M')
        is_valid = date_from <= date_to

        if not is_valid:
            self.add_error('date_from', f'{date_from} <= {date_to}')

        return is_valid


def search_groups(request, student_id):
    """
    Renders the search groups view.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - render: The rendered search groups view.
    """
    if not Student.objects.filter(id=student_id).exists():
        return Http404(
            f'Student with id {student_id} does not exist'
        )
    form = SearchForm(request.POST or None)

    context = {
        'form': SearchForm(),
        'errors': form.errors
    }

    if request.method == 'POST' and form.is_valid():
        context['groups'] = get_filtered_groups(form)
        context['student_id'] = student_id

    return render(request, 'assistant/search_groups.html', context)


def as_string(value: Union[str, None]):
    """
        Converts a value to a string or an empty string if the value is None.

        Parameters:
        - value (Union[str, None]): The value to be converted.

        Returns:
        - str: The string representation of the value or an empty string if the value is None.

        """
    if value is None:
        value = ''
    return value


def get_filtered_groups(form: SearchForm) -> List[Group]:
    """
        Retrieves filtered groups based on the search form criteria.

        Parameters:
        - form (SearchForm): The search form containing filtering criteria.

        Returns:
        - List[Group]: The list of filtered groups.

        """
    date_from = datetime.datetime.strptime(form['date_from'].value(), '%H:%M')
    date_to = datetime.datetime.strptime(form['date_to'].value(), '%H:%M')

    group_code = as_string(form['group_code'].value())
    course_code = as_string(form['course_code'].value())

    teacher = form['teacher'].value()
    lecturings = Lecturing.objects.filter(teacher__name__exact=teacher).all()
    teacher_groups = [lecturing.group.code for lecturing in lecturings]

    day_of_week = as_string(form['day_of_week'].value()).lower()
    # Days of week are kept in abbreviated form in the database
    if day_of_week != '':
        day_of_week = day_of_week[:2]

    filters = {
        'start_time__gte': date_from, 'end_time__lte': date_to,
        'code__startswith': group_code, 'course__group__code__startswith': course_code,
        'day_of_week__startswith': day_of_week
    }

    if teacher_groups:
        filters['code__in'] = teacher_groups

    return Group.objects.filter(**filters).distinct().all()
