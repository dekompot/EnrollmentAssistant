import datetime
from typing import List, Union

from django.forms import forms, DateField, DateTimeField, DateTimeInput
from django.forms import ChoiceField, Select
from django.http import Http404, HttpResponse
from django.shortcuts import render

from assistant.enrollment.groupshandler import GroupsHandler
from assistant.models import DayOfWeek, Course, Lecturing, Student

from assistant.models import Timetable, EnrollmentRecord, Group, Teacher


def timetable(request, student_id):
    try:
        student_timetable = Timetable.objects.get(student_id=student_id)
    except Timetable.DoesNotExist:
        raise Http404("Student timetable does not exist")

    enrollment_records = EnrollmentRecord.objects.filter(timetable=student_timetable).all()

    context = {
        'student_groups': [enr.group for enr in enrollment_records],
        'student_id': student_id
    }

    return render(request, 'assistant/timetable.html', context)


def group_details(request, group_code: str):
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
    groups = Group.objects.all()
    return [('', '')] + [(group.code, group.code) for group in groups]


def get_courses():
    courses = Course.objects.all()
    return [('', '')] + [(course.code, course.code) for course in courses]


def get_teachers():
    teachers = Teacher.objects.all()
    return [('', '')] + [(teacher.name, teacher.name) for teacher in teachers]


def get_days_of_week():
    days_of_week = DayOfWeek.choices
    return [('', '')] + days_of_week


class SearchForm(forms.Form):
    group_code = ChoiceField(widget=Select, choices=get_groups, required=False)
    course_code = ChoiceField(widget=Select, choices=get_courses, required=False)
    teacher = ChoiceField(widget=Select, choices=get_teachers, required=False)
    date_from = DateTimeField(widget=DateTimeInput, input_formats=['%H:%M', ], initial='00:00')
    date_to = DateTimeField(widget=DateTimeInput, input_formats=['%H:%M', ], initial='23:59')
    day_of_week = ChoiceField(widget=Select, choices=get_days_of_week, required=False)

    def is_valid(self):
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

    if not Student.objects.filter(id=student_id).exists():
        return Http404(
            f'Student with id {student_id} does not exist'
        )

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            context = {
                'groups': get_filtered_groups(form),
                'student_id': student_id
            }
            return render(request, 'assistant/groups.html', context)
        else:
            return render(request, 'assistant/form_error.html', {'form': form})

    # GET request
    return render(request, 'assistant/search_groups.html', {'form': SearchForm()})


def as_string(value: Union[str, None]):
    if value is None:
        value = ''
    return value


def get_filtered_groups(form: SearchForm) -> List[Group]:

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