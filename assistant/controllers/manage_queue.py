import datetime
from typing import List

from django.forms import forms, ChoiceField, CharField, TextInput
from django.http import HttpResponse
from django.shortcuts import render, redirect

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission, Student
from assistant.queue.queue import set_early_permissions, add, remove, get_queue


def give_early_permission(request, student_id):
    """
    Gives early permission to a student and redirects to the queue view.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - redirect: Redirects to the 'queue' view.
    """
    set_early_permissions(student_id, True)
    return redirect('queue')


def remove_early_permission(request, student_id):
    """
    Removes early permission from a student and redirects to the queue view.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - redirect: Redirects to the 'queue' view.
    """
    set_early_permissions(student_id, False)
    return redirect('queue')


def add_to_queue(request, student_id):
    """
    Adds a student to the enrollment queue and redirects to the queue view.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - redirect: Redirects to the 'queue' view.
    """
    enrollment_id = 'summer-2022/2023'
    add(enrollment_id, student_id)
    return redirect('queue')


def remove_from_queue(request, student_id):
    """
    Removes a student from the enrollment queue and redirects to the queue view.

    Parameters:
    - request: The HTTP request object.
    - student_id (str): The ID of the student.

    Returns:
    - redirect: Redirects to the 'queue' view.
    """
    enrollment_id = 'summer-2022/2023'
    remove(enrollment_id, student_id)
    return redirect('queue')


def queue(request):
    """
    Renders the enrollment queue view.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - render: The rendered enrollment queue view.
    """
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
    """
    Form for searching students based on specified criteria.

    Attributes:
    - name (CharField): The field for entering the student's name.
    - id (CharField): The field for entering the student's ID.

    """
    name = CharField(widget=TextInput, required=False)
    id = CharField(widget=TextInput, required=False)


def search_students(request):
    """
    Renders the search students view.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - render: The rendered search students view.
    """
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
    """
    Retrieves filtered students based on the search form criteria.

    Parameters:
    - form (SearchForm): The search form containing filtering criteria.

    Returns:
    - List[Student]: The list of filtered students.

    """
    filters = {}
    name = form['name'].value()
    index = form['id'].value()

    filters['name__contains'] = name
    filters['id__contains'] = index

    return Student.objects.filter(**filters).all().order_by('name').distinct()
