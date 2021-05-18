from itertools import combinations

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from django.db.models import Q
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompAthlete, Weight
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.Person import Person
from sbs.services import general_methods
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.models.Activity import Activity
from sbs.Forms.ActivityForm import ActivityForm
from django.core import serializers

from datetime import date, datetime
from django.utils import timezone


import json



def api_faliyet(request):
    response = JsonResponse({
        'status': 'Success',
        'faliyet': serializers.serialize("json",Activity.objects.all()),

    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def api_musabaka(request):
    response = JsonResponse({
        'status': 'Success',
        'musabaka': serializers.serialize("json",Competition.objects.all()),

    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def city_count(request):


    if request.GET.get('city'):
        athletecout = Athlete.objects.filter(communication__city__name__icontains=request.GET.get('city')).count()
        coachcout = Coach.objects.filter(communication__city__name__icontains=request.GET.get('city')).count()
        refereecout = Judge.objects.filter(communication__city__name__icontains=request.GET.get('city')).count()
        sportsClub = SportsClub.objects.filter(
            communication__city__name__icontains=request.GET.get('city')).count()

        response = JsonResponse({
            'athlete': athletecout,
            'coach': coachcout,
            'referee': refereecout,
            'sportsClub': sportsClub,
            'message':'success',
        })
    else:
        response = JsonResponse({
            'message':'none'
        })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def count(request):

    total_club = SportsClub.objects.count()
    total_athlete = Athlete.objects.count()
    total_athlete_gender_man = Athlete.objects.filter(person__gender=Person.MALE).count()
    total_athlete_gender_woman = Athlete.objects.filter(person__gender=Person.FEMALE).count()
    total_club_user = SportClubUser.objects.count()
    total_coachs = Coach.objects.count()
    total_judge = Judge.objects.count()
    total_user = User.objects.count()


    response=JsonResponse({'status': 'Success',
                         'messages': 'Verilen degerler',
                         'total_club_user': total_club_user,
                         'total_club': total_club,
                         'total_athlete': total_athlete,
                         'total_coachs': total_coachs,
                         'total_athlete_gender_man': total_athlete_gender_man,
                         'total_athlete_gender_woman': total_athlete_gender_woman,
                         'total_judge': total_judge,
                         'total_user': total_user,
                         })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return  response