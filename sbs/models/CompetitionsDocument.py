from django.db import models


class CompetitionsDocument(models.Model):
    fiksur = 'fiksur'
    sonuc = 'sonuc'

    Type = (
        (fiksur, 'Fiksür'),
        (sonuc, 'Sonuç'),

    )
    file = models.FileField(upload_to='document/', null=False, blank=False, verbose_name='Document')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=20, blank=True, null=True, choices=Type)



    # def __str__(self):
    #     return '%s' % (self.name)
