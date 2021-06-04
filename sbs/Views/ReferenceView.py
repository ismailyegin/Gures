from itertools import combinations

from accounts.models import Forgot

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
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, CompAthlete, Weight, PreRegistration
from sbs.models.ReferenceReferee import ReferenceReferee
from sbs.models.ReferenceCoach import ReferenceCoach
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods

from sbs.Forms.UserSearchForm import UserSearchForm
from unicode_tr import unicode_tr
from datetime import date, datetime
from django.utils import timezone


@login_required
def hakemler(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    referee = ReferenceReferee.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')
        active = request.POST.get('is_active')
        if not (firstName or lastName or email or active):
            referee = ReferenceReferee.objects.all().order_by('status')
            test=ReferenceReferee.objects.filter(first_name__icontains=firstName)
        else:
            query = Q()
            if lastName:
                query &= Q(last_name__icontains=lastName)
            if firstName:
                query &= Q(first_name__icontains=firstName)
            if email:
                query &= Q(email__icontains=email)
            if active == '1':
                query &= Q(status=ReferenceCoach.WAITED)
            if active == '2':
                query &= Q(status=ReferenceCoach.APPROVED)
            if active == '3':
                query &= Q(status=ReferenceCoach.DENIED)
            referee = ReferenceReferee.objects.filter(query)

    return render(request, 'basvurular/hakembasvuru.html', {'referees': referee,
                                                            'user_form':user_form})
@login_required
def antroner(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    referee = ReferenceCoach.objects.none()
    user_form = UserSearchForm()
    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')
        active = request.POST.get('is_active')
        if not (firstName or lastName or email or active):
            referee = ReferenceCoach.objects.all()
        else:
            query = Q()
            if lastName:
                query &= Q(last_name__icontains=lastName)
            if firstName:
                query &= Q(first_name__icontains=firstName)
            if email:
                query &= Q(email__icontains=email)
            if active == '1':
                query &= Q(status=ReferenceCoach.WAITED)
            if active == '2':
                query &= Q(status=ReferenceCoach.APPROVED)
            if active == '3':
                query &= Q(status=ReferenceCoach.DENIED)
            referee = ReferenceCoach.objects.filter(query)
    return render(request, 'basvurular/antrenorbasvuru.html', {'referees': referee,
                                                               'user_form':user_form})


@login_required
def sporcular(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    referee = None
    return render(request, 'basvurular/sporcubasvuru.html', {'referees': referee})
