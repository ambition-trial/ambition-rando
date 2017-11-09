import os

from django.apps import AppConfig as DjangoAppConfig
from django.conf import settings


class AppConfig(DjangoAppConfig):
    name = 'ambition_rando'
    sid_list_model = 'ambition_rando.randomizationlist'
    history_model = 'ambition_rando.subjectrandomization'
    randomization_list_path = os.path.join(
        settings.ETC_DIR, settings.APP_NAME, 'randomization_list.csv')
