from ambition import ambition_sites, fqdn
from ambition_rando.import_randomization_list import import_randomization_list
from ambition_rando.models import RandomizationList
from edc_base.tests import SiteTestCaseMixin
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday


class AmbitionTestCaseMixin(SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = ambition_sites

    site_names = [s[1] for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.import_randomization_list:
            import_randomization_list(verbose=False)
        import_holidays()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()
