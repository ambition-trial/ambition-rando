import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'ambition_rando'

    randomization_list_path = os.path.join(
        settings.ETC_DIR, settings.APP_NAME, 'randomization_list.csv')
