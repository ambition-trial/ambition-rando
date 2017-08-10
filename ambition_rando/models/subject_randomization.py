from django.db import models
from django.core.validators import RegexValidator

from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_managers import HistoricalRecords
from edc_base.model_mixins.base_uuid_model import BaseUuidModel


class SubjectRandomizationManager(models.Manager):

    def get_by_natural_key(self, sid):
        return self.get(sid=sid)


class SubjectRandomization(BaseUuidModel):

    study_site = models.CharField(
        max_length=25)

    sid = models.IntegerField(
        verbose_name='SID',
        unique=True)

    rx = EncryptedCharField(
        verbose_name="Treatment Assignment")

    subject_identifier = models.CharField(
        max_length=25)

    randomization_datetime = models.DateTimeField()

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))])

    objects = SubjectRandomizationManager()

    history = HistoricalRecords()

    def natural_key(self):
        return (self.sid, )

    def __str__(self):
        return f'{self.subject_identifier} {self.rx} {self.study_site} {self.sid}'
