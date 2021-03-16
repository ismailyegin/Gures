import enum

from django.db import models


class Competitiontype(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return '%s ' % self.name
