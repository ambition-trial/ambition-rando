from django.apps import apps as django_apps
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from edc_base.utils import get_utcnow
from edc_registration.models import RegisteredSubject

from .constants import RANDOMIZED


class RandomizationError(Exception):
    pass


class SidListError(Exception):
    pass


class DuplicateRandomizationAttempt(ValidationError):
    pass


app_config = django_apps.get_app_config('ambition_rando')


class Randomizer:

    sid_model = app_config.sid_list_model
    history_model = app_config.history_model

    def __init__(self, subject_consent=None, randomization_datetime=None):
        self.history_obj = None
        self.randomization_datetime = randomization_datetime or get_utcnow()
        self.subject_consent = subject_consent
        self.subject_identifier = subject_consent.subject_identifier
        self.study_site = subject_consent.study_site
        self.user = subject_consent.user_modified

        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.subject_identifier)
        if self.registered_subject.sid:
            self.history_obj = self.history_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        else:
            self.randomize()

    @property
    def sid(self):
        """Returns the SID.
        """
        return self.history_obj.sid

    def check_sid_model(self):
        if self.sid_model_cls.objects.all().count() == 0:
            raise SidListError(
                f'Randomization list has not been loaded. '
                f'Run the management command.')

    def randomize(self):
        """Returns a history model instance after selecting
        the next available SID.
        """
        try:
            self.history_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            list_obj = self.allocate_next()
            self.history_obj = self.history_model_cls.objects.create(
                study_site=list_obj.site,
                sid=list_obj.sid,
                rx=list_obj.drug_assigment,
                subject_identifier=self.subject_identifier,
                initials=self.subject_consent.initials,
                randomization_datetime=self.randomization_datetime)
            self.update_registered_subject()
        else:
            raise DuplicateRandomizationAttempt(
                f'Subject already listed as randomized. '
                f'Got \'{self.subject_identifier}\'. '
                f'See {self.history_model_cls}.',
                code=self.history_model)
        return self.history_obj

    def allocate_next(self):
        """Gets the next available SID and updates the list_obj
        as allocated to the subject.
        """
        sid_obj = self.get_next_sid()
        sid_obj.subject_identifier = self.subject_identifier
        sid_obj.allocated = True
        sid_obj.allocated_datetime = self.randomization_datetime
        sid_obj.allocated_user = self.user
        sid_obj.save()
        sid_obj = self.sid_model_cls.objects.get(
            subject_identifier=self.subject_identifier)
        return sid_obj

    def get_next_sid(self):
        """Gets the next available SID (sid_obj) or raises.
        """
        sid_obj = None
        self.check_sid_model()
        if self.sid_model_cls.objects.all().count() == 0:
            raise SidListError(
                f'Randomization list has not been loaded. '
                f'Run the management command.')
        try:
            self.sid_model_cls.objects.get(
                subject_identifier=self.subject_identifier)
        except ObjectDoesNotExist:
            sid_obj = self.sid_model_cls.objects.filter(
                subject_identifier__isnull=True,
                site=self.study_site).order_by('sid').first()
            if not sid_obj:
                raise SidListError(
                    f'Randomization failed. No additional SIDs available for '
                    f'site \'{self.study_site}\'.')
        else:
            raise DuplicateRandomizationAttempt(
                f'Randomization failed. Subject already listed as randomized. '
                f'Got \'{self.subject_identifier}\'. See {self.sid_model_cls}.',
                code=self.sid_model)
        return sid_obj

    def update_registered_subject(self):
        """Updates and requeries registered_subject.
        """
        self.registered_subject.sid = self.history_obj.sid
        self.registered_subject.randomization_datetime = (
            self.history_obj.randomization_datetime)
        self.registered_subject.registration_status = RANDOMIZED
        self.registered_subject.save()
        self.registered_subject = RegisteredSubject.objects.get(
            subject_identifier=self.subject_identifier)

    @property
    def history_model_cls(self):
        return django_apps.get_model(self.history_model)

    @property
    def sid_model_cls(self):
        return django_apps.get_model(self.sid_model)
