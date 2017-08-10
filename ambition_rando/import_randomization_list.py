import csv
import os
import sys

from django.conf import settings
from django.core.management.color import color_style

from .models import RandomizationList

style = color_style()


class RandomizationListImportError(Exception):
    pass


def import_randomization_list(path=None):
    """Imports CSV.

    Format:
        sid,drug_assigment,site
        1,single_dose,40
        2,two_doses,40
        ...
    """

    path = path or os.path.join(
        settings.BASE_DIR, 'test_randomization_list.csv')
    if RandomizationList.objects.all().count() > 0:
        raise RandomizationListImportError(
            'Not importing CSV. RandomizationList model is not empty!')
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            RandomizationList.objects.create(**row)
    count = RandomizationList.objects.all().count()
    sys.stdout.write(style.SUCCESS(
        f'(*) Imported {count} SIDs from {path}.\n'))
