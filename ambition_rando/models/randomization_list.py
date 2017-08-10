from django.db import models
from edc_base.model_mixins import BaseUuidModel


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

    drug_assigment = models.CharField(max_length=25)

    site = models.CharField(max_length=25)

    allocated = models.BooleanField(default=False)

    allocated_datetime = models.DateTimeField(null=True)

    allocated_user = models.CharField(max_length=50, null=True)

    verified = models.BooleanField(default=False)

    verified_datetime = models.DateTimeField(null=True)

    verified_user = models.CharField(max_length=50, null=True)

    def __str__(self):
        return f'{self.sid} subject={self.subject_identifier}'

    def natural_key(self):
        return (self.sid, )

    class Meta:
        ordering = ('sid', )
        unique_together = ('subject_identifier', 'sid')
