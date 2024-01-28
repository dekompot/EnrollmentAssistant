from django.shortcuts import render

from assistant.enrollment.enrollment import Enrollment
from assistant.models import Student, Group
from assistant.users import check_student_permission


@check_student_permission('CBE-2021-inz')
def register(request, field_of_studies, student_id, group_code):
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
    enrollment = Enrollment(field_of_studies)

    student = Student.objects.get(id=student_id)
    group = Group.objects.get(code=group_code)

    context = {
        'result': enrollment.unregister(student, group),
        'student': student, 'group': group
    }

    return render(request, 'assistant/unregister_result.html', context)

