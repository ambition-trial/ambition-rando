from ambition_sites import ambition_sites, fqdn
from edc_base import get_utcnow
from edc_base.tests import SiteTestCaseMixin
from edc_facility.import_holidays import import_holidays
from edc_facility.models import Holiday
from faker import Faker
from model_mommy import mommy

from ..randomization_list_importer import RandomizationListImporter
from ..models import RandomizationList

fake = Faker()


class AmbitionTestCaseMixin(SiteTestCaseMixin):

    fqdn = fqdn

    default_sites = ambition_sites

    site_names = [s[1] for s in default_sites]

    import_randomization_list = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        if cls.import_randomization_list:
            RandomizationListImporter(verbose=False)
        import_holidays(test=True)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        RandomizationList.objects.all().delete()
        Holiday.objects.all().delete()

    def create_subject(self, consent_datetime=None, first_name=None):
        consent_datetime = consent_datetime or get_utcnow()
        first_name = first_name or fake.first_name()
        subject_screening = mommy.make_recipe(
            "ambition_screening.subjectscreening", report_datetime=consent_datetime
        )
        consent = mommy.make_recipe(
            "ambition_subject.subjectconsent",
            screening_identifier=subject_screening.screening_identifier,
            consent_datetime=consent_datetime,
            first_name=first_name,
        )
        return consent.subject_identifier
