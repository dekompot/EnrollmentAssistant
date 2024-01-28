import datetime

from django.forms import forms, ChoiceField
from django.http import HttpResponse
from django.shortcuts import render, redirect

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission, Student


def give_early_permission(request, student_id):
    set_early_permissions(student_id, True)
    return redirect('queue')

def remove_early_permission(request, student_id):
    set_early_permissions(student_id, False)
    return redirect('queue')


def add_to_queue(request, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permission = EnrollmentPermission(queue=queue, student_id=student_id, date_from=datetime.datetime.now(), date_to=datetime.datetime.now())
    permission.save()
    return redirect('queue')


def remove_from_queue(request, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.delete()
    return redirect('queue')


def set_early_permissions(student_id, new_early_permission: bool):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.is_permitted_earlier = new_early_permission
    permissions.save()


def queue(request):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.filter(queue=queue)
    early = [permission.student for permission in permissions if  permission.is_permitted_earlier]
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

        return is_valid