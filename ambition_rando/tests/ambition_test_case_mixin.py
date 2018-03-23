from ambition import ambition_sites
from ambition_rando.import_randomization_list import import_randomization_list
from ambition_rando.models import RandomizationList
from django.contrib.sites.models import Site
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday


class AmbitionTestCaseMixin:

    default_sites = ambition_sites

    site_names = [s[1] for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Site.objects.all().delete()
        for site_id, site_name, _ in cls.default_sites:
            Site.objects.create(
                pk=site_id, name=site_name, domain=f'{site_name}.ambition.org.bw')
        if cls.import_randomization_list:
            import_randomization_list(verbose=False)
        import_holidays()

    @classmethod
    def tearDownClass(cls):
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()
        super().tearDownClass()
