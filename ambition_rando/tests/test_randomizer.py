import os

from django.apps import apps as django_apps
from django.test import TestCase, tag
from edc_registration.models import RegisteredSubject
from random import shuffle

from ..import_randomization_list import import_randomization_list
from ..models import RandomizationList
from ..randomizer import RandomizationError, AllocationError
from ..randomizer import Randomizer, RandomizationListError, AlreadyRandomized
from ..verify_randomization_list import verify_randomization_list
from .make_test_list import make_test_list, default_sites
from .models import SubjectConsent


class TestRandomizer(TestCase):

    def populate_list(self):
        path, filename = make_test_list()
        import_randomization_list(path=path, filename=filename, overwrite=True)

    def test_with_consent_no_site(self):
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345')
        self.assertRaises(
            RandomizationListError,
            Randomizer,
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)

    def test_with_consent(self):
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='10')
        self.assertRaises(
            RandomizationListError,
            Randomizer,
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)

    def test_with_list_selects_first(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        first_obj = RandomizationList.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        self.assertEqual(rando.sid, first_obj.sid)

    def test_updates_registered_subject(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        first_obj = RandomizationList.objects.all().first()
        rs = RegisteredSubject.objects.get(subject_identifier='12345')
        self.assertEqual(rs.subject_identifier, first_obj.subject_identifier)
        self.assertEqual(rs.sid, str(first_obj.sid))
        self.assertEqual(rs.randomization_datetime,
                         first_obj.allocated_datetime)

    def test_updates_list_obj_as_allocated(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        RandomizationList.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        first_obj = RandomizationList.objects.all().first()
        self.assertEqual(
            first_obj.subject_identifier, '12345')
        self.assertTrue(first_obj.allocated)
        self.assertIsNotNone(first_obj.allocated_user)
        self.assertEqual(first_obj.allocated_user,
                         subject_consent.user_modified)
        self.assertEqual(first_obj.allocated_datetime,
                         subject_consent.consent_datetime)
        self.assertGreater(first_obj.modified,
                           subject_consent.created)

    def test_cannot_rerandomize(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        first_obj = RandomizationList.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        self.assertEqual(rando.sid, first_obj.sid)
        self.assertRaises(
            AlreadyRandomized,
            Randomizer,
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)

    def test_error_condition1(self):
        """Assert raises if RegisteredSubject not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        with self.assertRaises(AlreadyRandomized) as cm:
            Randomizer(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                study_site=subject_consent.study_site,
                user=subject_consent.user_modified)
        self.assertEqual(cm.exception.code,
                         'ambition_rando.randomizationlist')

    def test_error_condition2(self):
        """Assert raises if RandomizationList not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        with self.assertRaises(AlreadyRandomized) as cm:
            Randomizer(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                study_site=subject_consent.study_site,
                user=subject_consent.user_modified)
        self.assertEqual(cm.exception.code,
                         'ambition_rando.randomizationlist')

    def test_error_condition3(self):
        """Assert raises if RandomizationList not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        RandomizationList.objects.update(subject_identifier=None)
        with self.assertRaises(AlreadyRandomized) as cm:
            Randomizer(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                study_site=subject_consent.study_site,
                user=subject_consent.user_modified)
        self.assertEqual(cm.exception.code,
                         'edc_registration.registeredsubject')

    def test_subject_does_not_exist(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        RegisteredSubject.objects.all().delete()
        self.assertRaises(
            RandomizationError,
            Randomizer,
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)

    def test_str(self):
        self.populate_list()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)
        obj = RandomizationList.objects.all().first()
        self.assertTrue(str(obj))

    @tag('1')
    def test_for_sites(self):
        """Assert that allocates by site correctly.
        """
        self.populate_list()

        sites = default_sites * 5
        shuffle(sites)
        # consent and randomize 5 for each site
        for index, study_site in enumerate(sites):
            subject_consent = SubjectConsent.objects.create(
                subject_identifier=f'12345{index}',
                study_site=study_site)
            Randomizer(
                subject_identifier=subject_consent.subject_identifier,
                report_datetime=subject_consent.consent_datetime,
                study_site=subject_consent.study_site,
                user=subject_consent.user_modified)

        # assert consented subjects were allocated SIDs in the
        # correct order per site.
        for site in default_sites:
            randomized_subjects = [
                (obj.subject_identifier, str(obj.sid)) for obj in
                RandomizationList.objects.filter(
                    site=site, subject_identifier__isnull=False).order_by('sid')]
            for index, obj in enumerate(
                    SubjectConsent.objects.filter(
                        study_site=site).order_by('consent_datetime')):
                rs = RegisteredSubject.objects.get(
                    subject_identifier=obj.subject_identifier)
                self.assertEqual(obj.subject_identifier,
                                 randomized_subjects[index][0])
                self.assertEqual(rs.sid, randomized_subjects[index][1])

        # clear out any unallocated
        RandomizationList.objects.filter(
            subject_identifier__isnull=True).delete()

        # assert raises on next attempt to randomize
        subject_consent = SubjectConsent.objects.create(
            subject_identifier=f'ABCDEF',
            study_site=study_site)
        self.assertRaises(
            AllocationError,
            Randomizer,
            subject_identifier=subject_consent.subject_identifier,
            report_datetime=subject_consent.consent_datetime,
            study_site=subject_consent.study_site,
            user=subject_consent.user_modified)

    @tag('2')
    def test_verify_list(self):

        message = verify_randomization_list()
        self.assertIn('Randomization list has not been loaded', message)

        # populate
        path1, filename1 = make_test_list(count=5)
        import_randomization_list(
            path=path1, filename=filename1, overwrite=True)
        self.assertEqual(RandomizationList.objects.all().count(), 5)

        # set to invalid path
        django_apps.app_configs[
            'ambition_rando'].randomization_list_path = '/tmp/erik.csv'
        message = verify_randomization_list()
        self.assertIn('Randomization list file does not exist', message)

        # change to a different assignments
        drug_assignments = ['up', 'down']
        path, filename = make_test_list(
            drug_assignments=drug_assignments, count=5)
        django_apps.app_configs[
            'ambition_rando'].randomization_list_path = os.path.join(path, filename)
        message = verify_randomization_list()
        self.assertIn('Randomization list is INVALID', message or '')

        # change to a different starting SID
        path2, filename2 = make_test_list(count=5, first_sid=100)
        django_apps.app_configs[
            'ambition_rando'].randomization_list_path = os.path.join(path2, filename2)
        message = verify_randomization_list()
        self.assertIn('Randomization list has INVALID SIDs', message or '')

        # change to a different starting SID
        django_apps.app_configs[
            'ambition_rando'].randomization_list_path = os.path.join(path1, filename1)
        message = verify_randomization_list()
        self.assertIsNone(message)

        # change number of SIDs in DB
        RandomizationList.objects.create(
            sid=100, drug_assignment='single_dose', site='40')
        self.assertEqual(RandomizationList.objects.all().count(), 6)
        message = verify_randomization_list()
        self.assertIn('Randomization list count is off', message)
