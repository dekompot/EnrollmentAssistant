from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime

from assistant.enrollment.enrollment import get_enrollment_edition
from assistant.models import Student, EnrollmentPermission
from assistant.timetable.student_utils import is_student_in_registration_period
from utils.return_codes import PermissionsReturnCodes


# Create user and save to the database
def create_user():
    user = User.objects.create_user('266640', '266640@email.com', 'mypassword')

    # Update fields and then save again
    user.first_name = 'Kacper'
    user.last_name = 'Bartoha'
    user.save()


def get_user(request, id : str = '266640'):
    if not User.objects.filter(username=id).exists():
        create_user()
    return User.objects.get(username=id)


def check_student_permission(field_of_studies: str):

    def decorator(function):

        def wrapper(request, *args, **kwargs):

            student_id = kwargs['student_id']
            permission_code = is_student_in_registration_period(student_id, field_of_studies)

            if permission_code == PermissionsReturnCodes.PERMITTED:
                return function(request, field_of_studies, *args, **kwargs)
            else:
                context = {'student_id' : kwargs['student_id'],
                           'permissions': [permission_code]}
                return render(request, 'shared/permission_denied.html', context)

        return wrapper

    return decorator

