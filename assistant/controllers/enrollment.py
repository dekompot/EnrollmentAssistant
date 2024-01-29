from django.shortcuts import render

from assistant.enrollment.enrollment import Enrollment
from assistant.models import Student, Group, DayOfWeek
from assistant.users import check_student_permission


@check_student_permission('CBE-2021-inz')
def register(request, field_of_studies, student_id, group_code):
    """
    View to register a student for a specific group.

    Parameters:
    - request: The HTTP request object.
    - field_of_studies (str): The field of studies associated with the student's permission.
    - student_id (str): The ID of the student.
    - group_code (str): The code of the group to register for.

    Returns:
    - render: The rendered registration result view.

    This view checks if the student has permission to register based on the provided field of studies.
    It then uses the `Enrollment` class to register the student for the specified group and renders
    the registration result view with relevant information.
    """
    enrollment = Enrollment(field_of_studies)

    student = Student.objects.get(id=student_id)
    group = Group.objects.get(code=group_code)
    context = {
        'result': enrollment.register(student, group).name,
        'student': student, 'group': group
    }

    return render(request, 'assistant/register_result.html', context)


@check_student_permission('CBE-2021-inz')
def unregister(request, field_of_studies, student_id, group_code):
    """
    View to unregister a student from a specific group.

    Parameters:
    - request: The HTTP request object.
    - field_of_studies (str): The field of studies associated with the student's permission.
    - student_id (str): The ID of the student.
    - group_code (str): The code of the group to unregister from.

    Returns:
    - render: The rendered unregistration result view.

    This view checks if the student has permission to unregister based on the provided field of studies.
    It then uses the `Enrollment` class to unregister the student from the specified group and renders
    the unregistration result view with relevant information.
    """
    enrollment = Enrollment(field_of_studies)

    student = Student.objects.get(id=student_id)
    group = Group.objects.get(code=group_code)

    context = {
        'result': enrollment.unregister(student, group),
        'student': student, 'group': group
    }

    return render(request, 'assistant/unregister_result.html', context)

