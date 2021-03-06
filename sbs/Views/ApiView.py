from itertools import combinations
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from django.db.models import Q
from sbs.models.SportsClub import SportsClub
from sbs.models.SportClubUser import SportClubUser
from sbs.models.Competition import Competition
from sbs.models.Athlete import Athlete
from sbs.models.Coach import Coach
from sbs.models.Judge import Judge
from sbs.models.Person import Person
from sbs.models.Success import Success
from sbs.models.CompetitionsAthlete import CompetitionsAthlete
from sbs.models.Activity import Activity
from django.core import serializers
from datetime import date, datetime
from django.utils import timezone
from unicode_tr import unicode_tr
def api_faliyet(request):
    response = JsonResponse({
        'status': 'Success',
        'faliyet': serializers.serialize("json", Activity.objects.all()),

    })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def detail_activity(request):
    if request.GET.get('id'):
        if Activity.objects.filter(pk=request.GET.get('id')):
            activity=Activity.objects.get(pk=request.GET.get('id'))
            response = JsonResponse({
                'status': True,
                'pk':activity.pk,
                'creationDate':activity.creationDate,
                'startDate':activity.startDate,
                'finishDate':activity.finishDate,
                'name':activity.name,
                'eventPlace':activity.eventPlace,
                'year':activity.year,
                'compType':activity.compType,
                'type':activity.type.name,

            })
    else:
        response = JsonResponse({
            'message': 'none'
        })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def api_musabaka(request):
    response = JsonResponse({
        'status': 'Success',
        'musabaka': serializers.serialize("json", Competition.objects.all()),

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
            'message': 'success',
        })
    else:
        response = JsonResponse({
            'message': 'none'
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
    response = JsonResponse({'status': 'Success',
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
    return response
def api_musabaka_basvuru(request):
    if Competition.objects.filter(registerStartDate__lte=timezone.now(), registerFinishDate__gte=timezone.now()):
        musabaka = \
        Competition.objects.filter(registerStartDate__lte=timezone.now(), registerFinishDate__gte=timezone.now())[0]

        catagori=""
        foto = ""
        fiksur = ""
        sonuc = ""
        for item in musabaka.categoryies.all():
            catagori+=item.kategoriadi+"/"
        for item in musabaka.file.all():
            if item.type == 'fiksur':
                foto += str(item.file) + "/"
            elif item.type == 'sonuc':
                sonuc += str(item.file) + "/"
            elif item.type == 'fotogaleri':
                foto += str(item.file) + "/"
        response = JsonResponse({
            'status': True,
            'finishdate': musabaka.finishDate.strftime("%d-%B-%Y"),
            'startDate': musabaka.startDate.strftime("%d-%B-%Y"),
            'registerStartDate': musabaka.registerStartDate.strftime("%d-%B-%Y") if musabaka.registerStartDate else None,
            'registerFinishDate': musabaka.registerFinishDate.strftime("%d-%B-%Y") if musabaka.registerFinishDate else None,
            'name': musabaka.name,
            'eventPlace': musabaka.eventPlace,
            'explanation': musabaka.explanation,
            'compType': musabaka.compType,
            'compGeneralType': musabaka.compGeneralType.name,
            'stil': list(musabaka.stil.all().values('name')),
            'kategori': list(musabaka.categoryies.all().values('kategoriadi')),
            'id': musabaka.pk,
            "foto": list(musabaka.file.filter(type="fotogaleri").values('file')),
            "sonuc": list(musabaka.file.filter(type="sonuc").values('file')),
            "fiksur": list(musabaka.file.filter(type="fiksur").values('file')),
            "haber": str(musabaka.haber),

            "youtubelink":list(musabaka.youtubelink.all().values('youtubelink'))



        })
    else:
        response = JsonResponse({
            'status':False,
        })

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def competitionsDetail(request):
    if request.GET.get('id'):
        if Competition.objects.filter(pk=request.GET.get('id')):
            musabaka=Competition.objects.get(pk=request.GET.get('id'))


            response = JsonResponse({
                'status': True,
                'finishdate': musabaka.finishDate.strftime("%d-%B-%Y"),
                'startDate': musabaka.startDate.strftime("%d-%B-%Y"),
                'registerStartDate': musabaka.registerStartDate.strftime("%d-%B-%Y") if musabaka.registerStartDate else None,
                'registerFinishDate': musabaka.registerFinishDate.strftime("%d-%B-%Y") if musabaka.registerFinishDate else None,
                'name': musabaka.name,
                'eventPlace': musabaka.eventPlace,
                'explanation': musabaka.explanation,
                'compType': musabaka.compType,
                'compGeneralType':musabaka.compGeneralType.name,
                'stil': musabaka.stil,
                'kategori': list(musabaka.categoryies.all().values('kategoriadi')),
                'id': musabaka.pk,
                "foto":list(musabaka.file.filter(type="fotogaleri").values('file')),
                "sonuc":list(musabaka.file.filter(type="sonuc").values('file')),
                "fiksur":list(musabaka.file.filter(type="fiksur").values('file')),
                "haber":str(musabaka.haber),
                "basvurulink": str(musabaka.basvurulink),
                "youtubelink": str(musabaka.youtubelink)

            })
    else:
        response = JsonResponse({
            'message': 'none'
        })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def club_result(request):


    sportclupArray=[]
    for item in SportsClub.objects.all():
        beka = {
            'id': item.pk,
            'name': item.name

        }
        sportclupArray.append(beka)

    response = JsonResponse({'status': 'Success',

                             'sportclub':sportclupArray,

                             })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
def club_return(request):
    sportclupArray=[]
    for item in SportsClub.objects.all():
        beka = {
            'id': item.pk,
            'name': item.name

        }
        sportclupArray.append(beka)

    response = JsonResponse({'status': 'Success',

                             'sportclub':sportclupArray,

                             })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response


def competition_search (request):
    name=None
    startDate=None
    compGeneralType=None
    compType=None
    musabaka =Competition.objects.none()

    if request.GET.get('name'):
        name = request.GET.get('name')
    if request.GET.get('year'):
        startDate = request.GET.get('year')
    if request.GET.get('compGeneralType'):
        compGeneralType = request.GET.get('compGeneralType')
    if request.GET.get('compType'):
        compType = request.GET.get('compType')

    if name or startDate or compGeneralType or compType:
        query = Q()
        if name:
            query &= Q(name__icontains=name)
        if startDate:
            query &= Q(finishDate__year=int(startDate))
        if compGeneralType:
            query &= Q(compGeneralType=compGeneralType)
        if compType:
            query &= Q(compType=compType)

        musabaka = Competition.objects.filter(query).order_by('-startDate').distinct()
    else:
        musabaka = Competition.objects.all().order_by('-startDate')

    list=[]
    if musabaka:
        for item in musabaka:
            beka = {

                'name': item.name,
                'startdate': item.startDate.strftime("%d-%B-%Y"),
                'finishDate': item.finishDate.strftime("%d-%B-%Y"),
                'registerStartDate': item.registerStartDate.strftime("%d-%B-%Y") if item.registerStartDate else None,
                'registerFinishDate': item.registerFinishDate.strftime("%d-%B-%Y") if item.registerFinishDate else None,
                'eventPlace': item.eventPlace,
                'haber': item.haber,
                'compType': item.compType,
                'compGeneralType': item.compGeneralType.name,
                'pk':item.pk,


            }
            list.append(beka)
    response = JsonResponse({'status': 'Success',

                             'results':list,

                             })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response
def club_search(request):
    firstName=None
    lastName=None
    cinsiyet=None
    club_id=None
    email=None
    tcno=None
    pk=None

    athlete =Athlete.objects.none()

    if request.GET.get('isim'):
        firstName=unicode_tr(request.GET.get('isim')).upper()
    if request.GET.get('soyisim'):
        lastName=unicode_tr(request.GET.get('soyisim')).upper()
    if request.GET.get('cinsiyet'):
        cinsiyet=int(request.GET.get('cinsiyet'))
    if request.GET.get('kulup'):
        club_id=int(request.GET.get('kulup'))
    if request.GET.get('email'):
        email=request.GET.get('email')
    if request.GET.get('tcno'):
        tcno=request.GET.get('tcno')
    if request.GET.get('pk'):
        pk=request.GET.get('pk')

    test=Athlete.objects.filter(person__gender=Person.FEMALE)


    if cinsiyet !=None or firstName or lastName or club_id !=None or tcno or email or pk:
        query = Q()
        if firstName:
            query &= Q(user__first_name__icontains=firstName)
        if tcno:
            query &= Q(person__tc__icontains=tcno)
        if lastName:
            query &= Q(user__last_name__icontains=lastName)
        if email:
            query &= Q(user__email__icontains=email)
        if club_id:
            query &= Q(licenses__sportsClub_id=club_id)
        if pk:
            query &= Q(pk=pk)
        if cinsiyet == 1:
            query &= Q(person__gender=Person.MALE)
        if cinsiyet == 0:
            query &= Q(person__gender=Person.FEMALE)
        athlete = Athlete.objects.filter(query).distinct()

    else:
        athlete=Athlete.objects.all()

    list=[]
    if athlete:
        for item in athlete:
            if item.licenses.filter(isActive=True):
                club=item.licenses.filter(isActive=True).last().sportsClub
                beka = {
                    'name': item.user.first_name,
                    'lastname': item.user.last_name,
                    'clubName': club.name,
                    'clubPk': club.pk,
                    'pk': item.pk,
                    'cinsiyet':item.person.gender,
                    'image':str(item.person.profileImage)


                }
            else:
                beka = {
                    'name': item.user.first_name,
                    'lastname': item.user.last_name,
                    'clubName': 'None',
                    'clubPk': 'None',
                    'pk': item.pk,
                    'cinsiyet': item.person.gender,
                    'image': str(item.person.profileImage)
                }

            list.append(beka)
    response = JsonResponse({'status': 'Success',
                             'results':list,
                             })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def search(list, platform):
    for i in range(len(list)):
        if list[i] == platform:
            return True
    return False

def competition_year(request):
    if Competition.objects.all():
        list = []
        for item in Competition.objects.all().order_by("-startDate"):
            if not(search(list, item.startDate.year)):
                list.append(item.startDate.year)
        response = JsonResponse({
            'year':list,
        })
    else:
        response = JsonResponse({
            'year': 'null',
        })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def medal_result(request):
    if Success.objects.all():
        list = []
        for item in Success.objects.all():
            beka={
                'type':item.type,
                'gold':item.gold,
                'silver':item.silver,
                'bronze':item.bronze
            }
            list.append(beka)
        response = JsonResponse({
            'medal':list,
        })
    else:
        response = JsonResponse({
            'medal': 'null',
        })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response

def return_competition_athlete(request):
    if request.GET.get('pk') and Competition.objects.filter(pk=request.GET.get('pk')):
        list = []
        for item in CompetitionsAthlete.objects.filter(competition=Competition.objects.get(pk=request.GET.get('pk'))):
            beka = {
                'isim': item.athlete.user.get_full_name(),
                'musabaka': item.competition.name,
                'siklet': item.siklet.weight,
                'year': item.category.kategoriadi,
                'derece': item.degree
            }
            list.append(beka)
        response = JsonResponse({
            'athlete': list,
        })
    else:
        response = JsonResponse({
            'athlete': 'null',
        })

    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response



def search_activity(request):
    name = request.GET.get('name')
    startDate = request.GET.get('startDate')
    compType = request.GET.get('compType')
    finishDate = request.GET.get('finishDate')
    year=request.GET.get('year')
    a_type = request.GET.get('type')
    if startDate == '0':
        startDate=None
    if compType == '0':
        compType=None
    if finishDate == '0':
        finishDate =None
    if a_type == '0':
        a_type=None
    if startDate:
        startDate = datetime.strptime(startDate, '%d/%m/%Y').date()
    if finishDate:
        finishDate = datetime.strptime(finishDate, "%d/%m/%Y").date()
    if name or startDate or compType or finishDate or a_type or year:
        query = Q()
        if name:
            query &= Q(name__icontains=name)
        if startDate and startDate !='0':
            query &= Q(startDate__gte=startDate)
        if compType :
            query &= Q(compType=compType)
        if finishDate:
            query &= Q(finishDate__lte=finishDate)
        if a_type:
            query &= Q(type__id=a_type)
        if year:
            query &= Q(year=year)
        activitys = Activity.objects.filter(query).distinct()
    else:
        activitys = Activity.objects.all()

    list=[]
    if activitys:
        for activity in activitys:
            beka={

                'status': True,
                'pk':activity.pk,
                'creationDate':activity.creationDate,
                'startDate':activity.startDate.strftime("%d-%B-%Y") if activity.startDate else None,
                'finishDate':activity.finishDate.strftime("%d-%B-%Y") if activity.finishDate else None,
                'name':activity.name,
                'eventPlace':activity.eventPlace,
                'year':activity.year,
                'compType':activity.compType,
                'type':activity.type.name,
            }
            list.append(beka)
    response = JsonResponse({'status': 'Success',
                             'results':list,
                             })
    response["Access-Control-Allow-Origin"] = "*"
    response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS"
    response["Access-Control-Max-Age"] = "1000"
    response["Access-Control-Allow-Headers"] = "*"
    return response







