import enum

from django.db import models

from sbs.models.Weight import Weight
from sbs.models.Coach import Coach
from sbs.models.Athlete import Athlete
from sbs.models.SportsClub import SportsClub
from sbs.models.Competition import Competition
from sbs.models.Category import Category


class CompetitionsAthlete(models.Model):
    creationDate = models.DateTimeField(auto_now_add=True)
    operationDate = models.DateTimeField(auto_now=True)

    coach = models.ForeignKey(Coach, on_delete=models.SET_NULL, null=True)
    athlete = models.ForeignKey(Athlete, on_delete=models.SET_NULL, related_name='athlete', null=True)
    club = models.ForeignKey(SportsClub, on_delete=models.SET_NULL, null=True)
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True)
    siklet = models.ForeignKey(Weight, on_delete=models.SET_NULL, null=True)
    degree = models.IntegerField(default=0)
    category=models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return '%s ' % self.coach

    # class Meta:
    #     default_permissions = ()
