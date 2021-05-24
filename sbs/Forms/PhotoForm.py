from django import forms
from django.forms import ModelForm

from sbs.models.CompetitionPhotoDocument import CompetitionPhotoDocumentDocument


class PhotoForm(ModelForm):
    class Meta:
        model = CompetitionPhotoDocumentDocument

        fields = (
             'file',
             'date')

        labels = {
                  'file': 'Dosya Seçiniz',
                  'date':'Tarihi Seçiniz',


                  }

        widgets = {

            'date': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask datepicker6', 'autocomplete': 'off',
                       'required': 'required'}),


        }
