import csv
import os
import sys

from django.conf import settings
from django.core.management.color import color_style

from .models import RandomizationList
from django.core.exceptions import ObjectDoesNotExist

style = color_style()


class RandomizationListImportError(Exception):
    pass


def import_randomization_list(path=None, verbose=None, overwrite=None, add=None):
    """Imports CSV.

    Format:
        sid,drug_assignment,site_name
        1,single_dose,gaborone
        2,two_doses,gaborone
        ...
    """

    verbose = True if verbose is None else verbose
    path = path or os.path.join(settings.RANDOMIZATION_LIST_PATH)
    path = os.path.expanduser(path)
    if overwrite:
        RandomizationList.objects.all().delete()
    if RandomizationList.objects.all().count() > 0 and not add:
        raise RandomizationListImportError(
            'Not importing CSV. RandomizationList model is not empty!')
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        sids = [row['sid'] for row in reader]
    if len(sids) != len(list(set(sids))):
        raise RandomizationListImportError(
            'Invalid file. Detected duplicate SIDs')
    with open(path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = {k: v.strip() for k, v in row.items()}
            try:
                RandomizationList.objects.get(sid=row['sid'])
            except ObjectDoesNotExist:
                RandomizationList.objects.create(**row)
    count = RandomizationList.objects.all().count()
    if verbose:
        sys.stdout.write(style.SUCCESS(
            f'(*) Imported {count} SIDs from {path}.\n'))
