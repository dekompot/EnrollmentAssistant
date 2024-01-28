import datetime
from typing import List

from django.forms import forms, ChoiceField, CharField, TextInput
from django.http import HttpResponse
from django.shortcuts import render, redirect

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission, Student
from assistant.queue.queue import set_early_permissions, add, remove, get_queue


def give_early_permission(request, student_id):
    set_early_permissions(student_id, True)
    return redirect('queue')


def remove_early_permission(request, student_id):
    set_early_permissions(student_id, False)
    return redirect('queue')


def add_to_queue(request, student_id):
    enrollment_id = 'summer-2022/2023'
    add(enrollment_id, student_id)
    return redirect('queue')


def remove_from_queue(request, student_id):
    enrollment_id = 'summer-2022/2023'
    remove(enrollment_id, student_id)
    return redirect('queue')


def queue(request):
    enrollment_id = 'summer-2022/2023'
    early, normal = get_queue('summer-2022/2023')
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    context = {
        'enrollment_edition': enrollment_edition.id,
        'field': enrollment_edition.field_of_studies.name,
        'normal': normal,
        'early': early
    }
    return render(request, 'queue/queue.html', context)


class SearchForm(forms.Form):
    name = CharField(widget=TextInput, required=False)
    id = CharField(widget=TextInput, required=False)


def search_students(request):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    form = SearchForm(request.POST or None)
    context = {
        'form': SearchForm(),
        'errors': form.errors
    }

    if request.method == 'POST':
        context['students'] = get_filtered_students(form)

    return render(request, 'assistant/search_students.html', context)


def get_filtered_students(form: SearchForm) -> List[Student]:
    filters = {}
    name = form['name'].value()
    index = form['id'].value()

    filters['name__contains'] = name
    filters['id__contains'] = index

    return Student.objects.filter(**filters).all().order_by('name').distinct()
