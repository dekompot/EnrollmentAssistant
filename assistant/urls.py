from django.urls import path


from .controllers.shared import timetable, search_groups, group_details
from .controllers.enrollment import register, unregister

urlpatterns = [
    path("timetable/<str:student_id>/", timetable, name="timetable"),
    path("enrollment/search/<str:student_id>/", search_groups, name="search_groups"),
    path("enrollment/details/<str:group_code>", group_details, name="group_details"),
    path("enrollment/register/<str:student_id>/<str:group_code>", register, name="register"),
    path("enrollment/unregister/<str:student_id>/<str:group_code>", unregister, name="unregister")
]