from datetime import datetime

from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission


def set_early_permissions(student_id, new_early_permission: bool):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if not contains(queue, student_id):
        add(enrollment_edition.id, student_id)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.is_permitted_earlier = new_early_permission
    permissions.save()


def add(enrollment_id, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if not contains(queue, student_id):
        permission = EnrollmentPermission(queue=queue, student_id=student_id, date_from=datetime.now(),
                                      date_to=datetime.now())
        permission.save()


def remove(enrollment_id, student_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    if contains(queue, student_id):
        permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
        permissions.delete()


def contains(queue, student_id):
    return EnrollmentPermission.objects.filter(queue=queue, student_id=student_id).count() == 1



def get_queue(enrollment_id):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact=enrollment_id)
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.filter(queue=queue)
    early = [permission.student for permission in permissions if permission.is_permitted_earlier]
    normal = [permission.student for permission in permissions if not permission.is_permitted_earlier]
    early = sorted(early, key=lambda s: s.average, reverse=True)
    normal = sorted(normal, key=lambda s: s.average, reverse=True)
    return early, normal
