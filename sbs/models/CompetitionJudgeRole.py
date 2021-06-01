from django.db import models

from sbs.models.Judge import Judge
from sbs.models.JudgeRole import JudgeRole


class CompetitionJudgeRole(models.Model):
    role = models.ForeignKey(JudgeRole,on_delete=models.SET_NULL,null=True,blank=True)
    judge=models.ForeignKey(Judge,on_delete=models.SET_NULL,null=True, blank=True)

    creationDate = models.DateTimeField(db_column='creationDate', blank=True, null=True, auto_now_add=True)
    # Field name made lowercase.
    operationDate = models.DateTimeField(db_column='operationDate', blank=True, null=True,
                                         auto_now_add=True)