from django import forms
from django.forms import ModelForm

from sbs.models.ActivityType import ActivityType

class ActivityTypeForm(ModelForm):
    class Meta:
        model = ActivityType

        fields = (
            'name',)

        labels = {'name':'Tanınmı'}

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),


        }
