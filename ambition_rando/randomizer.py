from edc_randomization.randomizer import Randomizer as Base

from .constants import CONTROL, SINGLE_DOSE


class Randomizer(Base):

    name = "ambition"
    assignment_map = {CONTROL: 1, SINGLE_DOSE: 2}
