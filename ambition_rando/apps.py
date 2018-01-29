import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings
from django.core.checks.registry import register

from .system_checks import randomization_list_check


class AppConfig(DjangoAppConfig):
    name = 'ambition_rando'
    include_in_administration = False

    def ready(self):
        register(randomization_list_check)

    @property
    def randomization_list_path(self):
        return os.path.join(settings.RANDOMIZATION_LIST_PATH)
