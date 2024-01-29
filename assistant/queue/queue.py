from datetime import datetime

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission


def set_early_permissions(student_id, new_early_permission: bool):
    """
    Sets or removes early enrollment permissions for a student in a specific enrollment edition.

    Parameters:
    - student_id (str): The ID of the student.
    - new_early_permission (bool): The new status of early enrollment permission.

    Returns:
    - None
    """
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if not contains(queue, student_id):
        if not new_early_permission:
            return
        add(enrollment_edition.id, student_id)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.is_permitted_earlier = new_early_permission
    permissions.save()


def add(enrollment_id, student_id):
    """
    Adds a student to the enrollment queue for a specific enrollment edition.

    Parameters:
    - enrollment_id (str): The ID of the enrollment edition.
    - student_id (str): The ID of the student.

    Returns:
    - None
    """
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if not contains(queue, student_id):
        permission = EnrollmentPermission(queue=queue, student_id=student_id, date_from=datetime.now(),
                                      date_to=datetime.now())
        permission.save()


def remove(enrollment_id, student_id):
    """
    Removes a student from the enrollment queue for a specific enrollment edition.

    Parameters:
    - enrollment_id (str): The ID of the enrollment edition.
    - student_id (str): The ID of the student.

    Returns:
    - None
    """
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if contains(queue, student_id):
        permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
        permissions.delete()


def contains(queue, student_id):
    """
    Checks if a student is in the enrollment queue.

    Parameters:
    - queue (EnrollmentQueue): The enrollment queue.
    - student_id (str): The ID of the student.

    Returns:
    - bool: True if the student is in the queue, False otherwise.
    """
    return EnrollmentPermission.objects.filter(queue=queue, student_id=student_id).count() == 1


def get_queue(enrollment_id):
    """
   Retrieves the enrollment queue for a specific enrollment edition.

   Parameters:
   - enrollment_id (str): The ID of the enrollment edition.

   Returns:
   - Tuple[List[Student], List[Student]]: Two lists representing students with early and normal enrollment permissions.
   """
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.filter(queue=queue)
    early = [permission.student for permission in permissions if permission.is_permitted_earlier]
    normal = [permission.student for permission in permissions if not permission.is_permitted_earlier]
    early = sorted(early, key=lambda s: s.average, reverse=True)
    normal = sorted(normal, key=lambda s: s.average, reverse=True)
    return early, normal
