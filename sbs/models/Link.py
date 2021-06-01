from django.db import models


class Link(models.Model):
    definition = models.CharField(max_length=200, blank=False, null=False)
    youtubelink=models.CharField(max_length=200, blank=False, null=False)
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True, auto_now_add=True)
    # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase.

    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
