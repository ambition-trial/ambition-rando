from django.apps import apps as django_apps
from django.views.generic.base import ContextMixin


class RandomizationListViewMixin(ContextMixin):

    randomization_list_model = 'ambition_rando.randomizationlist'

    @property
    def treatment_description(self):
        model_cls = django_apps.get_model(self.randomization_list_model)
        obj = model_cls.objects.get(
            subject_identifier=self.kwargs.get('subject_identifier'))
        return obj.treatment_description

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(treatment_description=self.treatment_description)
        return context
