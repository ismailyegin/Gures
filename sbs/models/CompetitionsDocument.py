from django.db import models


class CompetitionsDocument(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)
    name = models.FileField(upload_to='competitions/', null=False, blank=False, verbose_name='file')

    def __str__(self):
        return '%s' % (self.name)
