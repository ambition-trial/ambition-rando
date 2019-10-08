from ambition_sites import ambition_sites

from .constants import SINGLE_DOSE, CONTROL


class InvalidDrugAssignment(Exception):
    pass


def get_assignment(row):
    """Returns assignment as a word; 'single_dose' or 'control'.

    Converts a numeric assignment or allocation
    to a word.
    """
    assignment = row["assignment"]
    if assignment not in [SINGLE_DOSE, CONTROL]:
        if int(row["assignment"]) == 2:
            assignment = SINGLE_DOSE
        elif int(row["assignment"]) == 1:
            assignment = CONTROL
        else:
            raise InvalidDrugAssignment(
                f"Invalid assignment. " f'Got \'{row["assignment"]}\'. Expected 1 or 2.'
            )
    return assignment


def get_allocation(row, assignment):
    """Returns an allocation as 1 or 2 for the given
    assignment or raises.
    """

    try:
        allocation = row["orig_allocation"]
    except KeyError:
        if assignment == SINGLE_DOSE:
            allocation = "2"
        elif assignment == CONTROL:
            allocation = "1"
        else:
            raise InvalidDrugAssignment(f"Invalid assignment. Got {assignment}.")
    return allocation


def get_site_name(long_name, row=None):
    """Returns the site name given the "long" site name.
    """
    try:
        site_name = [site for site in ambition_sites if site[2] == long_name][0][1]
    except IndexError as e:
        raise IndexError(f"{long_name} not found. Got {e}. See {row}")
    return site_name
