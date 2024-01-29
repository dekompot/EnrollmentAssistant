import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'EnrollmentAssistant.settings'
django.setup()
pydoc.cli()