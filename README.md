[![Build Status](https://travis-ci.org/ambition-study/ambition-rando.svg?branch=develop)](https://travis-ci.org/ambition-study/ambition-rando) [![Coverage Status](https://coveralls.io/repos/github/ambition-study/ambition-rando/badge.svg?branch=develop)](https://coveralls.io/github/ambition-study/ambition-rando?branch=develop)

# ambition-rando

Randomization class and model for Ambition


To rebuild the records in RandomizationList:

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.models import Site
from edc_registration.models import RegisteredSubject
from ambition_rando.models import RandomizationList

current_site = Site.objects.get_current()
for obj in RegisteredSubject.on_site.all():
    try:
        randobj = RandomizationList.objects.get(sid=obj.sid)
    except ObjectDoesNotExist:
        print(f'missing for {obj.subject_identifier}, {obj.sid}.')
    else:
        randobj.alocated_site=current_site
        randobj.subject_identifier=obj.subject_identifier
        randobj.allocated_datetime=obj.consent_datetime
        randobj.allocated=True
        randobj.save() 
