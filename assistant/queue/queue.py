from assistant.models import EnrollmentEdition, EnrollmentQueue, EnrollmentPermission


def set_early_permissions(student_id, new_early_permission: bool):
    enrollment_edition = EnrollmentEdition.objects.get(id__exact='summer-2022/2023')
    queue = EnrollmentQueue.objects.get(enrollment_edition=enrollment_edition)
    permissions = EnrollmentPermission.objects.get(queue=queue, student=student_id)
    permissions.is_permitted_earlier = new_early_permission
    permissions.save()