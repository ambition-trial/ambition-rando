from django import forms

from .models import SubjectRandomization


class SubjectRandomizationForm(forms.ModelForm):

    class Meta:
        model = SubjectRandomization
        fields = '__all__'
