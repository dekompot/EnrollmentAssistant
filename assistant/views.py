from django.shortcuts import render

# Create your views here.
from django.http import Http404
from django.views import generic

from assistant.models import Timetable, EnrollmentRecord, Group

