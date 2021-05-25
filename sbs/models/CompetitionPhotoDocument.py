from django.db import models


class CompetitionPhotoDocumentDocument(models.Model):

    file = models.FileField(upload_to='document/', null=False, blank=False, verbose_name='Document')
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name='photoAciklama')

    # def __str__(self):
    #     return '%s' % (self.name)