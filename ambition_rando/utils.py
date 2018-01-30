from ambition.sites import ambition_sites

from .constants import SINGLE_DOSE, CONTROL


def get_drug_assignment(row):
    """Returns drug_assignment as a word; 'single_dose' or 'control'.

    Converts a numeric drug_assignment or allocation
    to a word.
    """
    drug_assignment = row['drug_assignment']
    if drug_assignment not in [SINGLE_DOSE, CONTROL]:
        if int(row['drug_assignment']) == 2:
            drug_assignment = SINGLE_DOSE
        elif int(row['drug_assignment']) == 1:
            drug_assignment = CONTROL
        else:
            raise TypeError('Invalid drug assignment')
    return drug_assignment


def get_site_name(long_name, row=None):
    """Returns the site name given the "long" site name.
    """
    try:
        site_name = [site for site in ambition_sites if site[2]
                     == long_name][0][1]
    except IndexError as e:
        raise IndexError(f'{long_name} not found. Got {e}. See {row}')
    return site_name
