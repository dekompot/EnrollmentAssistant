from django.shortcuts import render

from assistant.enrollment.enrollment import Enrollment
from assistant.models import Student, Group


def register(request, student_id, group_code):
    enrollment = Enrollment('CBE-2021-inz')

    student = Student.objects.get(id=student_id)
    group = Group.objects.get(code=group_code)

    context = {
        'result': enrollment.register(student, group).name,
        'student': student, 'group': group
    }

    return render(request, 'assistant/register_result.html', context)


def unregister(request, student_id, group_code):
    enrollment = Enrollment('CBE-2021-inz')

    student = Student.objects.get(id=student_id)
    group = Group.objects.get(code=group_code)

    context = {
        'result': enrollment.unregister(student, group),
        'student': student, 'group': group
    }

    return render(request, 'assistant/unregister_result.html', context)

