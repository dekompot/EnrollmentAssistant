from django.urls import path


from .controllers.shared import timetable, search_groups, group_details

urlpatterns = [
    path("timetable/<str:student_id>/", timetable, name="timetable"),
    path("enrollment/search", search_groups, name="search_groups"),
    path("enrollment/details/<str:group_code>", group_details, name="group_details")
]