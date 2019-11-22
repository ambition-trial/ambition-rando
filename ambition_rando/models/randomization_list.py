from django_crypto_fields.fields import EncryptedTextField
from edc_model.models import BaseUuidModel
from edc_randomization.models import RandomizationListModelMixin
from edc_randomization.randomizer import RandomizationError
from edc_randomization.site_randomizers import site_randomizers

from ..constants import CONTROL, CONTROL_NAME, SINGLE_DOSE, SINGLE_DOSE_NAME


class RandomizationListModelError(Exception):
    pass


class RandomizationList(RandomizationListModelMixin, BaseUuidModel):

    randomizer_cls = site_randomizers.get("ambition")

    assignment = EncryptedTextField(
        choices=((SINGLE_DOSE, SINGLE_DOSE_NAME), (CONTROL, CONTROL_NAME)),
    )

    allocation = EncryptedTextField(
        verbose_name="Original integer allocation", null=True
    )

    @property
    def assignment_description(self):
        if self.assignment == CONTROL:
            return CONTROL_NAME
        elif self.assignment == SINGLE_DOSE:
            return SINGLE_DOSE_NAME
        raise RandomizationError(f"Invalid assignment. Got {self.assignment}")

    class Meta(RandomizationListModelMixin.Meta):
        pass
