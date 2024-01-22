import os

from django.template.backends import django
from django.test import TestCase

from parsing.parse_json import load_grid_from_json




# Create your tests here.
if __name__ == '__main__':

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
    django.settings.configure()

    load_grid_from_json(enrollment_edition_id='summer-2022/2023', file='assistant/data/plan_kacpra.json', save_to_db=False)