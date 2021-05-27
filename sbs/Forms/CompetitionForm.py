from django import forms
from django.forms import ModelForm

from sbs.models import Competition


class CompetitionForm(ModelForm):
    class Meta:
        model = Competition

        fields = (
            'name', 'startDate', 'finishDate', 'compType', 'eventPlace',
            'registerStartDate', 'registerFinishDate', 'youtubelink','basvurulink','compGeneralType','stil')

        labels = {'name': 'İsim', 'startDate': 'Başlangıç Tarihi', 'finishDate': 'Bitiş Tarihi',
                  'eventPlace': 'Etkinlik Yeri',
                  'registerStartDate': 'Ön Kayıt Başlangıç Tarihi',
                  'registerFinishDate': 'Ön Kayıt Bitiş Tarihi',
                  'youtubelink': 'Youtube Link ',
                  'basvurulink': 'Başvuru Link ',
                  'compGeneralType':'Genel Tür ',
                  'compType': 'Türü',
                  'stil':'Stil',


                  }

        widgets = {

            'registerStartDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),
            'registerFinishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datepicker6', 'autocomplete': 'on',
                       'onkeydown': 'return true'}),

            'eventPlace': forms.TextInput(attrs={'class': 'form-control', "style": "text-transform:uppercase"}),

            'youtubelink': forms.TextInput(attrs={'class': 'form-control'}),
            'basvurulink': forms.TextInput(attrs={'class': 'form-control'}),

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker2', 'autocomplete': 'on',
                       'required': 'required'}),

            'finishDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right datemask', 'id': 'datepicker4', 'autocomplete': 'on',
                       'required': 'required'}),

            'name': forms.TextInput(
                attrs={'class': 'form-control', 'required': 'required', "style": "text-transform:uppercase"}),

            'compType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%;' , 'required': 'required'}),
            'compGeneralType': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                            'style': 'width: 100%; ', 'required': 'required'}),
            'stil': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; ',}),

        }
