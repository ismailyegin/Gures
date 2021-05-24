from django.db import models


class CompetitionPhotoDocumentDocument(models.Model):

    file = models.FileField(upload_to='document/', null=False, blank=False, verbose_name='Document')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    date = models.DateTimeField( blank=True, null=True)

    # def __str__(self):
    #     return '%s' % (self.name)