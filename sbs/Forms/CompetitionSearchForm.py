from django import forms
from django.forms import ModelForm

from sbs.models import Competition


class CompetitionSearchForm(ModelForm):
    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate','compType','compGeneralType')

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Yılı ',
                  'compGeneralType': 'Genel Tür ',
                  'compType': 'Türü',
                  'finishDate':'Bitiş Tarihi'
                  }

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker3', 'autocomplete': 'on',
                       }),
            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right ', 'id': 'datepicker4', 'autocomplete': 'on',
                       }),

            'name': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'compType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;'}),
            'compGeneralType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}),

        }
