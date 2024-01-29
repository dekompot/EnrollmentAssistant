import django
import pydoc
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'dummy.settings'
django.setup()
pydoc.cli()