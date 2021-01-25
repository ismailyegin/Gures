from django import forms
from django.forms import ModelForm
from sbs.models import License, SportsClub

class LicenseForm(ModelForm):
    sportsClub = forms.ModelChoiceField(queryset=SportsClub.objects.all(),
                                        to_field_name='name',
                                        empty_label="Seçiniz",
                                        label="Kulübü*",
                                        # required=True,
                                        widget=forms.Select(
                                            attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                   'style': 'width: 100%; '}))

    class Meta:
        model = License

        fields = (
            'startDate', 'sportsClub', 'branch', 'licenseNo', 'cityHeadShip', 'expireDate', 'lisansPhoto')

        labels = {'startDate': 'Başlangıç Tarihi*', 'branch': 'Branş*',
                  'licenseNo': 'Lisans No*', 'cityHeadShip': 'Verildiği İl*', 'expireDate': 'Bitiş Tarihi*',
                  'lisansPhoto': 'Lisans Foto'}

        widgets = {

            'startDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker2', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),

            'expireDate': forms.DateInput(
                attrs={'class': 'form-control  pull-right', 'id': 'datepicker4', 'autocomplete': 'on',
                       'onkeydown': 'return true', 'required': 'required'}),

            'branch': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                          'style': 'width: 100%; '}),

            'licenseNo': forms.TextInput(
                attrs={'class': 'form-control', 'onkeypress': 'validate(event)', 'required': 'required'}),

            'cityHeadShip': forms.Select(attrs={'class': 'form-control select2 select2-hidden-accessible',
                                                'style': 'width: 100%;', 'required': 'required'}),




        }
