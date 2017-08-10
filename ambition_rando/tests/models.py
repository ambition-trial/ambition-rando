from django.db import models
from edc_base.model_mixins import BaseUuidModel
from edc_registration.model_mixins import UpdatesOrCreatesRegistrationModelMixin


class SubjectConsent(UpdatesOrCreatesRegistrationModelMixin, BaseUuidModel):

    study_site = models.CharField(max_length=25)

    subject_identifier = models.CharField(max_length=25)

    initials = models.CharField(max_length=25)
