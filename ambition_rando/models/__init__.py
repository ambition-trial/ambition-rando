from django.conf import settings

from .randomization_list import RandomizationList

if settings.APP_NAME == 'ambition_rando':
    from ..tests import models
