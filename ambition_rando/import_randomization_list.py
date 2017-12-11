import csv
import os
import sys

from django.conf import settings
from django.core.management.color import color_style

from .models import RandomizationList

style = color_style()


class RandomizationListImportError(Exception):
    pass


def import_randomization_list(path=None, verbose=None, overwrite=None, filename=None):
    """Imports CSV.

    Format:
        sid,drug_assignment,site
        1,single_dose,40
        2,two_doses,40
        ...
    """

    verbose = True if verbose is None else verbose
    filename = filename or settings.BASE_DIR or 'test_randomization_list.csv'
    path = os.path.expanduser(path)
    path = os.path.join(path, filename)
    if overwrite:
        RandomizationList.objects.all().delete()
    if RandomizationList.objects.all().count() > 0:
        raise RandomizationListImportError(
            'Not importing CSV. RandomizationList model is not empty!')
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            RandomizationList.objects.create(**row)
    count = RandomizationList.objects.all().count()
    if verbose:
        sys.stdout.write(style.SUCCESS(
            f'(*) Imported {count} SIDs from {path}.\n'))
