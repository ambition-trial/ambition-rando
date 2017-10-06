from django.contrib.admin import AdminSite


class EdcAmbitionRandoAdminSite(AdminSite):
    site_header = 'Ambition Rando'
    site_title = 'Ambition Randomization'
    index_title = 'Ambition Randomization'
    site_url = '/'


ambition_rando_admin = EdcAmbitionRandoAdminSite(
    name='ambition_rando_admin')
