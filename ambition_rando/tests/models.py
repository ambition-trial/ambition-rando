from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin
from edc_base.utils import get_utcnow


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    study_site = models.CharField(max_length=25)

    subject_identifier = models.CharField(max_length=25)

    initials = models.CharField(max_length=25)

    consent_datetime = models.DateTimeField(default=get_utcnow)
