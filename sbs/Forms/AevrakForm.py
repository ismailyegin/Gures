from django import forms
from django.forms import ModelForm

from sbs.models.Aevrak import Aevrak
from sbs.models.AbirimParametre import AbirimParametre
from sbs.models.Abirim import Abirim


class AevrakForm(ModelForm):

    def __init__(self, birim, *args, **kwargs):
        super(AevrakForm, self).__init__(*args, **kwargs)
        # print(birim)
        parametre = AbirimParametre.objects.filter(birim_id=birim)

        for item in parametre:
            # print(item.title)
            # print(item.type)
            if item.type == 'string':
                self.fields[item.title] = forms.CharField(max_length=200)
                self.fields[item.title].widget.attrs['class'] = 'form-control'
            elif item.type == 'date':
                self.fields[item.title] = forms.CharField()
                self.fields[item.title].widget.attrs['class'] = 'form-control  pull-right datepicker6'

            elif item.type == 'number':
                self.fields[item.title] = forms.CharField(max_length=200)
                self.fields[item.title].widget.attrs['onkeypress'] = 'validate(event)'
                self.fields[item.title].widget.attrs['class'] = 'form-control'
        #
        #
        #
        # for visible in self.visible_fields():
        #     visible.field.widget.attrs['class'] = 'form-control'

    def save(self):
        evrak = Aevrak()
        for item in self.changed_data:
            setattr(evrak, item, self.data[item])
        evrak.save()

    class Meta:
        model = Aevrak
        fields = ()
