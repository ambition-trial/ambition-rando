import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'ambition_rando'
    randomization_list_model = 'ambition_rando.randomizationlist'
    randomization_list_path = os.path.join(
        settings.ETC_DIR, 'randomization_list.csv')
