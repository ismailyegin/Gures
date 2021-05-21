from django import forms
from django.forms import ModelForm

from sbs.models.CompetitionsDocument import CompetitionsDocument


class CompetitionsDocumentForm(ModelForm):
    class Meta:
        model = CompetitionsDocument

        fields = (
             'file',
             'type')

        labels = {
                  'file': 'Dosya Seçiniz',
                  'type':'Dosya Türü Seçiniz'


                  }

        widgets = {


            'type': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'required': 'required'}),

        }
