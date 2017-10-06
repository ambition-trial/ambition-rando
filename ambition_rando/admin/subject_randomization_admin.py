from django.contrib import admin
from django.contrib import admin
from django.urls.base import reverse
from django.urls.exceptions import NoReverseMatch
from django_revision.modeladmin_mixin import ModelAdminRevisionMixin
from edc_base.fieldsets import FieldsetsModelAdminMixin
from edc_base.modeladmin_mixins import (
    ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
    ModelAdminFormAutoNumberMixin, ModelAdminAuditFieldsMixin,
    ModelAdminReadOnlyMixin, ModelAdminInstitutionMixin,
    FormAsJSONModelAdminMixin, ModelAdminRedirectOnDeleteMixin)
from edc_base.modeladmin_mixins import audit_fieldset_tuple
from edc_visit_tracking.modeladmin_mixins import (
    CrfModelAdminMixin as VisitTrackingCrfModelAdminMixin)

from ..admin_site import ambition_rando_admin
from ..forms import SubjectRandomizationForm
from ..models import SubjectRandomization


class ModelAdminMixin(ModelAdminNextUrlRedirectMixin, ModelAdminFormInstructionsMixin,
                      ModelAdminFormAutoNumberMixin, ModelAdminRevisionMixin,
                      ModelAdminAuditFieldsMixin, ModelAdminReadOnlyMixin,
                      ModelAdminInstitutionMixin):
    pass


@admin.register(SubjectRandomization, site=ambition_rando_admin)
class SubjectRandomizationAdmin(ModelAdminMixin, admin.ModelAdmin):

    form = SubjectRandomizationForm
