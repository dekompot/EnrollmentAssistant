from django.contrib.auth.models import User
from django.shortcuts import render
from datetime import datetime

from assistant.enrollment.enrollment import get_enrollment_edition
from assistant.models import Student, EnrollmentPermission
from assistant.timetable.student_utils import is_student_in_registration_period
from utils.return_codes import PermissionsReturnCodes


# Create user and save to the database
def create_user():
    """
    MOCK FUNCTION
    Creates a new user with predefined details and updates some fields.

    Returns:
    - None
    """
    user = User.objects.create_user('266640', '266640@email.com', 'mypassword')

    # Update fields and then save again
    user.first_name = 'Kacper'
    user.last_name = 'Bartoha'
    user.save()


def get_user(request, id : str = '266640'):
    """
    MOCK FUNCTION
    Retrieves a user with the specified username or creates a new one if not exists.
    """
    if not User.objects.filter(username=id).exists():
        create_user()
    return User.objects.get(username=id)


def check_student_permission(field_of_studies: str):
    """
    Decorator to check if a student has permission for a specific action based on the registration period.

    Parameters:
    - field_of_studies (str): The field of studies associated with the permission check.

    Returns:
    - decorator: The decorator function.

    Usage Example:
    ```
    @check_student_permission('CBE-2021-inz')
    def some_protected_view(request, field_of_studies, *args, **kwargs):
        # Your view logic here
    ```

    The decorator checks if the student has permission to perform the specified action
    based on the registration period for the given field of studies. If permission is granted,
    the wrapped view function is called; otherwise, a permission denied page is rendered.
    """
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

