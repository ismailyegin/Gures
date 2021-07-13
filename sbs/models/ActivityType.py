from django.db import models


class ActivityType(models.Model):
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True,
                                        auto_now_add=True)  # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase.

    name = models.CharField(db_column='activityTypeName', max_length=100, blank=False,
                            null=False)  # Field name made lowercase.

    def __str__(self):
        return '%s ' % self.name
