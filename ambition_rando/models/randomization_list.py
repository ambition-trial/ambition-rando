from django_crypto_fields.fields import EncryptedTextField
from edc_model.models import BaseUuidModel
from edc_randomization.models.model_mixin import RandomizationListModelMixin

from ..constants import CONTROL, CONTROL_NAME, SINGLE_DOSE, SINGLE_DOSE_NAME
from ..randomizer import Randomizer, RandomizationError


class RandomizationListModelError(Exception):
    pass


class RandomizationList(RandomizationListModelMixin, BaseUuidModel):

    randomizer_cls = Randomizer

    assignment = EncryptedTextField(
        choices=((SINGLE_DOSE, SINGLE_DOSE_NAME), (CONTROL, CONTROL_NAME))
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
