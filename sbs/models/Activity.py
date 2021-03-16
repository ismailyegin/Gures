

from django.db import models
from sbs.models.ActivityType import ActivityType
from sbs.models.CompetitionsDocument import CompetitionsDocument
class Activity(models.Model):
    type = models.ForeignKey(ActivityType, on_delete=models.CASCADE, null=False, blank=False)
    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True,
                                        auto_now_add=True)  # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase.
    startDate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.
    finishDate = models.DateTimeField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=False, null=False)
    eventPlace = models.CharField(db_column='eventPlace', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    year = models.IntegerField(blank=True, null=True)  # Field name made lowercase.

    files = models.ManyToManyField(CompetitionsDocument)

    def __str__(self):
        return '%s ' % self.name

    # def save(self, force_insert=False, force_update=False):
    #     if self.name:
    #         self.name = self.name.upper()
    #
    #     super(Activity, self).save(force_insert, force_update)
