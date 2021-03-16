from django import forms
from django.forms import ModelForm

from sbs.models.Material import Material


class MaterialForm(ModelForm):
    class Meta:
        model = Material

        fields = (
            'ayakkabi', 'esofman', 'tshirt', 'guresayakkabi', 'sporayakkabi', 'klasikayakkabi')
        labels = {'guresayakkabi': 'Güreş Ayakkabısı', 'sporayakkabi': 'Spor  Ayakkabı',
                  'klasikayakkabi': 'Klasik Ayakkabı',
                  'tshirt': 'Tshirt', 'esofman': 'Esofman', 'ayakkabi': 'Ayakkabi'}
        widgets = {

            'ayakkabi': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'esofman': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'tshirt': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

            'guresayakkabi': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),
            'sporayakkabi': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),
            'klasikayakkabi': forms.TextInput(attrs={'class': 'form-control ', "style": "text-transform:uppercase"}),

        }
