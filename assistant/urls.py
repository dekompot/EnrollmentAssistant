from django.urls import path

from . import views
from .views import GeneratePlanController

urlpatterns = [
    path("<int:student_id>/", GeneratePlanController.student, name="student")
]