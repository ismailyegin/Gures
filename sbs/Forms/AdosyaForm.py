from sbs.models import Abirim
from sbs.models.Adosya import Adosya
from django import forms
from django.forms import ModelForm
from sbs.models.AdosyaParametre import AdosyaParametre
from sbs.models.AbirimParametre import AbirimParametre


class AdosyaForm(ModelForm):

    def __init__(self, klasor, birim, *args, **kwargs):
        super(AdosyaForm, self).__init__(*args, **kwargs)
        # print(birim)
        parametre = AbirimParametre.objects.filter(birim_id=birim)
        print(parametre)

        for item in parametre:
            if item.type == 'string':
                self.fields[item.title] = forms.CharField(max_length=200)
                self.fields[item.title].widget.attrs['class'] = 'form-control'
                self.fields[item.title].widget.attrs['id'] = item.pk
            elif item.type == 'date':
                self.fields[item.title] = forms.CharField()
                self.fields[item.title].widget.attrs['class'] = 'form-control  pull-right datepicker6'
                self.fields[item.title].widget.attrs['id'] = item.pk
            elif item.type == 'number':
                self.fields[item.title] = forms.CharField(max_length=200)
                self.fields[item.title].widget.attrs['onkeypress'] = 'validate(event)'
                self.fields[item.title].widget.attrs['class'] = 'form-control'
                self.fields[item.title].widget.attrs['id'] = item.pk

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

    def save(self):

        for item in self.changed_data:
            dosyaParametre = AdosyaParametre(
                value=self.data[item],
                parametre=self.data['parametre']

            )
            dosyaParametre.save()

    class Meta:
        model = Adosya
        fields = ('sirano', 'klasor')
