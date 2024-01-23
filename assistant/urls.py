from django.urls import path

from . import views
from .controllers.shared import timetable, search_groups

urlpatterns = [
    path("timetable/<str:student_id>/", timetable, name="timetable"),
    path("enrollment/search", search_groups, name="search_groups")
]