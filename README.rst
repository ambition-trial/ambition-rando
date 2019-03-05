|pypi| |travis| |codecov| |downloads|


ambition-rando
--------------

Randomization class and model for Ambition

To load the randomization list:

.. code-block:: python

    python manage.py import_randomization_list


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
    
.. |travis| image:: https://travis-ci.com/ambition-trial/ambition-rando.svg?branch=develop
    :target: https://travis-ci.com/ambition-trial/ambition-rando
    
.. |codecov| image:: https://codecov.io/gh/ambition-trial/ambition-rando/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/ambition-trial/ambition-rando

.. |downloads| image:: https://pepy.tech/badge/ambition-rando
   :target: https://pepy.tech/project/ambition-rando
