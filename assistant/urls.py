from django.urls import path


from .controllers.shared import timetable, search_groups, group_details
from .controllers.enrollment import register, unregister
from .controllers.manage_queue import (queue, give_early_permission, remove_early_permission,
                                       add_to_queue, remove_from_queue)

urlpatterns = [
    path("timetable/<str:student_id>/", timetable, name="timetable"),
    path("enrollment/search/<str:student_id>/", search_groups, name="search_groups"),
    path("enrollment/details/<str:group_code>", group_details, name="group_details"),
    path("enrollment/register/<str:student_id>/<str:group_code>", register, name="register"),
    path("enrollment/unregister/<str:student_id>/<str:group_code>", unregister, name="unregister"),
    path("queue", queue, name="queue"),
    path("queue/early/<str:student_id>", give_early_permission, name="early"),
    path("queue/early-rm/<str:student_id>", remove_early_permission, name="rm-early"),
    path("queue/remove/<str:student_id>", remove_from_queue, name="remove"),
    path("queue/add/<str:student_id>", add_to_queue, name="add")
]