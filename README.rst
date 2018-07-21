|pypi| |travis| |coverage|


ambition-rando
--------------

Randomization class and model for Ambition


To rebuild the records in RandomizationList:

.. code-block:: python

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


.. |pypi| image:: https://img.shields.io/pypi/v/ambition-rando.svg
    :target: https://pypi.python.org/pypi/ambition-rando
    
.. |travis| image:: https://travis-ci.org/clinicedc/ambition-rando.svg?branch=develop
    :target: https://travis-ci.org/clinicedc/ambition-rando
    
.. |coverage| image:: https://coveralls.io/repos/github/clinicedc/ambition-rando/badge.svg?branch=develop
    :target: https://coveralls.io/github/clinicedc/ambition-rando?branch=develop
