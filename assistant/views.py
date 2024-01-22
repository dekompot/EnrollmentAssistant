from django.shortcuts import render

# Create your views here.
from django.http import Http404

from assistant.models import Timetable, EnrollmentRecord, Group


class GeneratePlanController:

    @staticmethod
    # /assistant/266593/
    def student(request, student_id):
        try:
            student_timetable = Timetable.objects.get(student_id=student_id)
        except Timetable.DoesNotExist:
            raise Http404("Question does not exist")

        enrollment_records = EnrollmentRecord.objects.filter(timetable=student_timetable).all()

        context = {
            'student_groups': [enr.group_code for enr in enrollment_records]
        }

        return render(request, 'assistant/student.html', context)

