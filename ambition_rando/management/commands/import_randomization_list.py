import os

from django.core.management.base import BaseCommand, CommandError

from ...import_randomization_list import import_randomization_list


class Command(BaseCommand):

    help = 'Import randomization list'

    def add_arguments(self, parser):
        parser.add_argument(
            '--path',
            dest='path',
            default=None,
            help=('full path to CSV file.'),
        )

    def handle(self, *args, **options):
        path = options['path']
        if not os.path.exists(path or ''):
            raise CommandError(f'Invalid path. Got {path}')
        import_randomization_list(path=path)
