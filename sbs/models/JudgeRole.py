from django.db import models

class JudgeRole(models.Model):
    name = models.CharField(max_length=45, blank=True, null=True)
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True, auto_now_add=True)
    # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase

    def __str__(self):
        return '%s' % (self.name)