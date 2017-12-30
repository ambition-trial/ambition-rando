from ambition_rando.import_randomization_list import import_randomization_list
from django.contrib.sites.models import Site
from ambition_rando.models import RandomizationList


class SiteTestCaseMixin:

    default_sites = [
        (10, 'mochudi'),
        (20, 'molepolole'),
        (30, 'lobatse'),
        (40, 'gaborone'),
        (50, 'karakobis')]

    site_names = [s[1] for s in default_sites]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Site.objects.all().delete()
        for site_id, site_name in cls.default_sites:
            Site.objects.create(
                pk=site_id, name=site_name, domain=f'{site_name}.ambition.org.bw')
        import_randomization_list(verbose=False)

    @classmethod
    def tearDownClass(cls):
        RandomizationList.objects.all().delete()
        super().tearDownClass()
