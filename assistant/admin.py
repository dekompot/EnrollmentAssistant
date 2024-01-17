import inspect

from django.contrib import admin
from assistant.models import *
from assistant import models
# Register your models here.

clsmembers = inspect.getmembers(models, inspect.isclass)

for _, clazz in clsmembers:
    try:
        admin.site.register(clazz)
    except Exception as e:
        print(e)


