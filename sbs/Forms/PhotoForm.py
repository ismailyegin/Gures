from django import forms
from django.forms import ModelForm

from sbs.models.CompetitionPhotoDocument import CompetitionPhotoDocumentDocument


class PhotoForm(ModelForm):
    class Meta:
        model = CompetitionPhotoDocumentDocument

        fields = (
             'file',
             'title')

        labels = {
                  'file': 'Dosya Seçiniz',
                  'title':'Tarihi Seçiniz',


                  }

        widgets = {

            'title': forms.TextInput(
                attrs={'class': 'form-control ', 'value': '', "style": "text-transform:uppercase"}),



        }
