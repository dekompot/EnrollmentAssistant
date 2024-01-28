import datetime
from typing import List

from django.forms import forms, ChoiceField, CharField, TextInput
from django.http import HttpResponse
from django.shortcuts import render, redirect

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission, Student
from assistant.queue.queue import set_early_permissions


def give_early_permission(request, student_id):
    set_early_permissions(student_id, True)
    return redirect('queue')


def remove_early_permission(request, student_id):
    set_early_permissions(student_id, False)
    return redirect('queue')


def add_to_queue(request, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permission = EnrollmentPermission(queue=queue, student_id=student_id, date_from=datetime.datetime.now(),
                                      date_to=datetime.datetime.now())
    permission.save()
    return redirect('queue')


def remove_from_queue(request, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.delete()
    return redirect('queue')





def queue(request):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.filter(queue=queue)
    early = [permission.student for permission in permissions if permission.is_permitted_earlier]
    normal = [permission.student for permission in permissions if not permission.is_permitted_earlier]
    early = sorted(early, key=lambda s: s.average, reverse=True)
    normal = sorted(normal, key=lambda s: s.average, reverse=True)
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
