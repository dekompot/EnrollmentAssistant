import datetime
from typing import List

from django.forms import forms, DateField, DateTimeField, DateTimeInput
from django.forms import ChoiceField, Select
from django.http import Http404, HttpResponse
from django.shortcuts import render
from assistant.models import DayOfWeek, Course, Lecturing

from assistant.models import Timetable, EnrollmentRecord, Group, Teacher


def timetable(request, student_id):
    try:
        student_timetable = Timetable.objects.get(student_id=student_id)
    except Timetable.DoesNotExist:
        raise Http404("Student timetable does not exist")

    enrollment_records = EnrollmentRecord.objects.filter(timetable=student_timetable).all()

    context = {
        'student_groups': [enr.group for enr in enrollment_records]
    }

    return render(request, 'assistant/timetable.html', context)


def get_groups():
    groups = Group.objects.all()
    return [('', '')] + [(group.code, group.code) for group in groups]


def get_courses():
    courses = Course.objects.all()
    return [('', '')] + [(course.code, course.code) for course in courses]


def get_teachers():
    teachers = Teacher.objects.all()
    return [('', '')] + [(teacher.name, str(teacher)) for teacher in teachers]


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
            return False

        group_code = self['group_code'].value()
        course_code = self['course_code'].value()
        is_valid = group_code == '' or course_code == ''

        if not is_valid:
            self.add_error('group_code', f"group_code = {group_code}, course_code = {course_code}")

        return is_valid


def search_groups(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            context = {
                'groups': get_filtered_groups(form)
            }
            return render(request, 'assistant/groups.html', context)
        else:
            return render(request, 'assistant/form_error.html', {'form': form})

    # GET request
    return render(request, 'assistant/search_groups.html', {'form': SearchForm()})


def get_filtered_groups(form: SearchForm) -> List[Group]:

    date_from = datetime.datetime.strptime(form['date_from'].value(), '%H:%M')
    date_to = datetime.datetime.strptime(form['date_to'].value(), '%H:%M')

    group_code = form['group_code'].value()
    course_code = form['group_code'].value()

    teacher = form['teacher'].value()
    lecturings = Lecturing.objects.filter(teacher__name__exact=teacher).all()

    return Group.objects.filter(start_time__gte=date_from, end_time__lte=date_to,
                                code__startswith=group_code, course__group__code__startswith=course_code).all()