import sys

from collections import namedtuple
from django.core.checks import Warning

from .verify_randomization_list import verify_randomization_list

err = namedtuple('Err', 'id cls')

error_configs = dict(
    randomization_list_check=err('ambition.W001', Warning),
)


def randomization_list_check(app_configs, **kwargs):
    errors = []
    error = error_configs.get('randomization_list_check')
    if 'test' not in sys.argv and 'makemigrations' not in sys.argv and 'migrate' not in sys.argv:
        error_msg = verify_randomization_list()
        if error_msg:
            errors.append(
                error.cls(
                    error_msg,
                    hint=None,
                    obj=None,
                    id=error.id,
                )
            )
    return errors
