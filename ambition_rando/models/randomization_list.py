from django.db import models
from django_crypto_fields.fields import EncryptedCharField
from edc_base.model_mixins import BaseUuidModel
from edc_base.model_managers import HistoricalRecords

from ..constants import CONTROL, CONTROL_NAME, SINGLE_DOSE, SINGLE_DOSE_NAME
from ..randomizer import RandomizationError


class RandomizationListManager(models.Manager):

    def get_by_natural_key(self, sid):
        return self.get(sid=sid)


class RandomizationList(BaseUuidModel):

    subject_identifier = models.CharField(
        verbose_name="Subject Identifier",
        max_length=50,
        null=True,
        unique=True)

    sid = models.IntegerField(unique=True)

    drug_assignment = EncryptedCharField()

    site = models.CharField(max_length=25)

    allocated = models.BooleanField(default=False)

    allocated_datetime = models.DateTimeField(null=True)

    allocated_user = models.CharField(max_length=50, null=True)

    verified = models.BooleanField(default=False)

    verified_datetime = models.DateTimeField(null=True)

    verified_user = models.CharField(max_length=50, null=True)

    objects = RandomizationListManager()

    history = HistoricalRecords()

    def __str__(self):
        return f'{self.sid} subject={self.subject_identifier}'

    @property
    def short_label(self):
        return (f'{self.drug_assignment} SID:{self.sid}')

    @property
    def treatment_description(self):
        if self.drug_assignment == CONTROL:
            return CONTROL_NAME
        elif self.drug_assignment == SINGLE_DOSE:
            return SINGLE_DOSE_NAME
        raise RandomizationError(
            f'Invalid drug assignment. Got {self.drug_assignment}')

    def natural_key(self):
        return (self.sid, )

    class Meta:
        ordering = ('site', 'sid', )
        unique_together = ('subject_identifier', 'sid')
