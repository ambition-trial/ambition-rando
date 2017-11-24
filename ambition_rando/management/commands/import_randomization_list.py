import os

from django.apps import apps as django_apps
from django.core.management.base import BaseCommand, CommandError

from ...import_randomization_list import import_randomization_list, RandomizationListImportError


class Command(BaseCommand):

    help = 'Import randomization list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            default=None,
            help=('full path to CSV file. Default: app_config.randomization_list_path'),
        )

        parser.add_argument(
            '--force-overwrite',
            dest='overwrite',
            default='NO',
            help=('overwrite existing data. CANNOT BE UNDONE!!'),
        )

    def handle(self, *args, **options):
        app_config = django_apps.get_app_config('ambition_rando')
        path = options['path'] or app_config.randomization_list_path
        if not os.path.exists(path or ''):
            raise CommandError(f'Invalid path. Got {path}')
        overwrite = options['overwrite'] if options['overwrite'] == 'YES' else None
        try:
            import_randomization_list(path=path, overwrite=overwrite)
        except RandomizationListImportError as e:
            raise CommandError(e)
