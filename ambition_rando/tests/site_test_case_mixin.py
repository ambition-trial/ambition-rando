from django.contrib.sites.models import Site


class SiteTestCaseMixin:

    default_sites = [
        (10, 'mochudi'),
        (20, 'molepolole'),
        (30, 'lobatse'),
        (40, 'gaborone'),
        (50, 'karakobis')]

    site_names = [s[1] for s in default_sites]

    def setUp(self):
        super().setUp()
        Site.objects.all().delete()
        for site_id, site_name in self.default_sites:
            Site.objects.create(
                pk=site_id, name=site_name, domain=f'{site_name}.ambition.org.bw')
