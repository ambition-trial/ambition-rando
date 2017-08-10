import csv
import os

from django.test import TestCase
from django.conf import settings
from edc_registration.models import RegisteredSubject

from ..models import RandomizationList, SubjectRandomization
from ..randomizer import Randomizer, RandomizationError
from ..randomizer import SidListError, DuplicateRandomizationAttempt
from .models import SubjectConsent


class TestRandomizer(TestCase):

    def populate_list(self):
        RandomizationList.objects.all().delete()
        path = os.path.join(settings.BASE_DIR, 'test_randomization_list.csv')
        with open(path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                RandomizationList.objects.create(**row)

    def test_with_consent_no_site(self):
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345')
        self.assertRaises(
            SidListError,
            Randomizer, subject_consent=subject_consent)

    def test_with_consent(self):
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='10')
        self.assertRaises(
            SidListError,
            Randomizer, subject_consent=subject_consent)

    def test_with_list_selects_first(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        first_obj = RandomizationList.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(subject_consent=subject_consent)
        self.assertEqual(rando.sid, first_obj.sid)

    def test_updates_registered_subject(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(subject_consent=subject_consent)
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
        Randomizer(subject_consent=subject_consent)
        first_obj = RandomizationList.objects.all().first()
        self.assertEqual(
            first_obj.subject_identifier, '12345')
        self.assertTrue(first_obj.allocated)
        self.assertIsNotNone(first_obj.allocated_user)
        self.assertEqual(first_obj.allocated_user,
                         subject_consent.user_modified)
        self.assertGreater(first_obj.allocated_datetime,
                           subject_consent.created)

    def test_cannot_rerandomize(self):
        self.populate_list()
        RandomizationList.objects.update(site='40')
        first_obj = RandomizationList.objects.all().first()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(subject_consent=subject_consent)
        self.assertEqual(rando.sid, first_obj.sid)
        rando = Randomizer(subject_consent=subject_consent)
        self.assertEqual(rando.sid, first_obj.sid)

    def test_error_condition1(self):
        """Assert raises if RegisteredSubject not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(subject_consent=subject_consent)
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        with self.assertRaises(DuplicateRandomizationAttempt) as cm:
            Randomizer(subject_consent=subject_consent)
        self.assertEqual(cm.exception.code,
                         'ambition_rando.subjectrandomization')

    def test_error_condition2(self):
        """Assert raises if RandomizationList not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(subject_consent=subject_consent)
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        SubjectRandomization.objects.update(sid=12345)
        with self.assertRaises(DuplicateRandomizationAttempt) as cm:
            Randomizer(subject_consent=subject_consent)
        self.assertEqual(cm.exception.code,
                         'ambition_rando.subjectrandomization')

    def test_error_condition3(self):
        """Assert raises if RandomizationList not updated correctly.
        """
        self.populate_list()
        RandomizationList.objects.update(site='40')
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        rando = Randomizer(subject_consent=subject_consent)
        rando.registered_subject.sid = None
        rando.registered_subject.save()
        RandomizationList.objects.update(subject_identifier=None)
        with self.assertRaises(DuplicateRandomizationAttempt) as cm:
            Randomizer(subject_consent=subject_consent)
        self.assertEqual(cm.exception.code,
                         'ambition_rando.subjectrandomization')

    def test_str(self):
        self.populate_list()
        subject_consent = SubjectConsent.objects.create(
            subject_identifier='12345',
            study_site='40')
        Randomizer(subject_consent=subject_consent)
        obj = RandomizationList.objects.all().first()
        self.assertTrue(str(obj))
        obj = SubjectRandomization.objects.all().first()
        self.assertTrue(str(obj))
