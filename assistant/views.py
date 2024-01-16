from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader

from assistant.models import Timetable, EnrollmentRecord, Group


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


# /assistant/266593/
def student(request, student_id):
    student_timetable = Timetable.objects.get(student_id=student_id)
    enrollment_records = EnrollmentRecord.objects.filter(timetable=student_timetable.id).all()

    student_groups = [enr.group_code for enr in enrollment_records]

    template = loader.get_template('assistant/student.html')
    context = {
        'student_groups': student_groups
    }

    return HttpResponse(template.render(context, request))