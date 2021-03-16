
from django.db import models

from sbs.models.Category import Category
from sbs.models.Judge import Judge
from sbs.models.Competitiontype import Competitiontype

from sbs.models.EnumFields import EnumFields
class Competition(models.Model):
    serbest = 'Serbest Stil'
    grokomen = 'Grokomen'
    kadın = 'Kadınlar'

    COMPTYPE = (
        (serbest, 'Serbest Stil'),
        (grokomen, 'Grokomen'),
        (kadın, 'Kadınlar'),

    )

    mider = 'Minder'
    yagli = 'Yağlı'
    karakucak = 'Karakucak'

    Type = (
        (mider, 'Minder'),
        (yagli, 'Yağlı'),
        (karakucak, 'Karakucak'),

    )

    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True, auto_now_add=True)
    # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)  # Field name made lowercase.

    finishDate = models.DateTimeField(db_column='finishDate', blank=True, null=True)  # Field name made lowercase.
    startDate = models.DateTimeField(db_column='startDate', blank=True, null=True)  # Field name made lowercase.

    registerStartDate = models.DateTimeField(db_column='registerStartDate', blank=True,
                                             null=True)  # Field name made lowercase.
    registerFinishDate = models.DateTimeField(db_column='registerFinishDate', blank=True,
                                              null=True)  # Field name made lowercase.
    name = models.CharField(max_length=255, blank=True, null=True)
    eventPlace = models.CharField(db_column='eventPlace', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.
    eskimi = models.BooleanField(default=True)
    explanation = models.CharField(max_length=20, blank=True, null=True)
    compGeneralType = models.ForeignKey(Competitiontype, on_delete=models.CASCADE, null=True, blank=True)

    compType = models.CharField(max_length=20, blank=True, null=True, choices=Type)

    stil = models.CharField(max_length=20, blank=True, null=True, choices=COMPTYPE)


    categoryies = models.ManyToManyField(Category)
    judges = models.ManyToManyField(Judge)


    def __str__(self):
        return '%s ' % self.name

    # class Meta:
    #     default_permissions = ()
