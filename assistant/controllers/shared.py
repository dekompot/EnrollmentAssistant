from typing import List

from django.forms import forms
from django.forms import ChoiceField, Select
from django.http import Http404, HttpResponse
from django.shortcuts import render

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
    return [(group.code, group.code) for group in groups]


def get_teachers():
    teachers = Teacher.objects.all()
    return [(teacher.name, str(teacher)) for teacher in teachers]


class SearchForm(forms.Form):
    group_code_field = ChoiceField(widget=Select, choices=get_groups)
    teacher_field = ChoiceField(widget=Select, choices=get_teachers)


def search_groups(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            context = {
                'groups': get_filtered_groups(form)
            }
            return render(request, 'assistant/groups.html', context)

    return render(request, 'assistant/search_groups.html', {'form': SearchForm()})


def get_filtered_groups(form: SearchForm) -> List[Group]:
    return Group.objects.all()