from builtins import print

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from datetime import timedelta, datetime
from django.core.mail import EmailMultiAlternatives

from sbs.Forms.CompetitionForm import CompetitionForm
from sbs.Forms.CompetitionSearchForm import CompetitionSearchForm
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.Forms.CompetitionsDocumentForm import CompetitionsDocumentForm
from sbs.Forms.PhotoForm import PhotoForm
from sbs.models import SportClubUser, SportsClub, Competition, Athlete, Weight, CompCategory, Coach
from sbs.models.Category import Category
from sbs.models.CompetitionStil import CompetitionStil
from sbs.models.CompetitionsAthlete import CompetitionsAthlete
from sbs.models.SandaAthlete import SandaAthlete
from sbs.models.SimpleCategory import SimpleCategory
from sbs.models.Judge import Judge
from sbs.models.Link import Link
from sbs.services import general_methods
from sbs.models.CompetitionsDocument import CompetitionsDocument
from sbs.models.CompetitionPhotoDocument import CompetitionPhotoDocumentDocument


from sbs.Forms.UserSearchForm import UserSearchForm
from unicode_tr import unicode_tr

# from pyexcel_xls import get_data as xls_get
# from pyexcel_xlsx import get_data as xlsx_get

from sbs.models.CompetitionJudgeRole import CompetitionJudgeRole
from sbs.models.JudgeRole import JudgeRole
@login_required
def categori_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    simplecategoryForm = SimplecategoryForm()
    categoryitem = SimpleCategory.objects.all()
    if request.method == 'POST':
        simplecategoryForm = SimplecategoryForm(request.POST)
        if simplecategoryForm.is_valid():
            simplecategoryForm.save()
            messages.success(request, 'Kategori Başarıyla Güncellenmiştir.')
        else:
            messages.warning(request, 'Birşeyler ters gitti yeniden deneyiniz.')

    return render(request, 'musabaka/musabaka-Simplecategori.html',
                  {'category_item_form': simplecategoryForm, 'categoryitem': categoryitem})


@login_required
def aplication(request, pk):
    perm = general_methods.control_access_klup(request)
    active = general_methods.controlGroup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)

    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    weights = Weight.objects.all()
    if active == 'KlupUye':
        sc_user = SportClubUser.objects.get(user=user)
        if sc_user.dataAccessControl == True:
            if active == 'KlupUye':
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)

                comAthlete = CompetitionsAthlete.objects.filter(competition=pk,
                                                                athlete__licenses__sportsClub__in=clubsPk).distinct()
        else:
            messages.warning(request, 'Lütfen Eksik olan Sporcu Bilgilerini tamamlayiniz.')
            return redirect('sbs:musabakalar')
    elif active == 'Yonetim' or active == 'Admin':
        comAthlete = CompetitionsAthlete.objects.filter(competition=pk).distinct()

    elif active == 'Antrenor':
        coach = Coach.objects.get(user=user)
        comAthlete = CompetitionsAthlete.objects.filter(competition=pk, athlete__licenses__coach=coach).distinct()
    return render(request, 'musabaka/basvuru.html',
                  {'athletes': comAthlete, 'competition': musabaka, 'weights': weights})


@login_required
def return_competition(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competitions = Competition.objects.filter(startDate__year=timezone.now().year)
    year = timezone.now().year
    year = Competition.objects.values('year').distinct().order_by('year')
    return render(request, 'musabaka/sonuclar.html', {'competitions': competitions, 'year': year})


@login_required
def return_competitions(request):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    comquery = CompetitionSearchForm()
    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),
                                             registerFinishDate__gte=timezone.now())
    competitions = Competition.objects.none()

    if request.method == 'POST':
        name = request.POST.get('name')
        startDate = request.POST.get('startDate')
        compGeneralType = request.POST.get('compGeneralType')
        compType = request.POST.get('compType')
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

            competitions = Competition.objects.filter(query).order_by('-startDate').distinct()
        else:
            competitions = Competition.objects.all().order_by('-startDate')
    return render(request, 'musabaka/musabakalar.html',
                  {'competitions': competitions, 'query': comquery,
                   'application': competition, 'user':request.user})


@login_required
def musabaka_ekle(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition_form = CompetitionForm()
    if request.method == 'POST':
        competition_form = CompetitionForm(request.POST)
        if competition_form.is_valid():
            musabaka = competition_form.save(commit=False)
            musabaka.juryCount = 0;
            musabaka.save()

            log = str(request.POST.get('name')) + "  Musabaka eklendi "
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Müsabaka Başarıyla Kaydedilmiştir.')

            return redirect('sbs:musabaka-duzenle', pk=musabaka.pk)
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'musabaka/musabaka-ekle.html',
                  {'competition_form': competition_form})


@login_required
def musabaka_duzenle(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    musabaka = Competition.objects.get(pk=pk)
    competition_form = CompetitionForm(request.POST or None, instance=musabaka)
    dokuman_form = CompetitionsDocumentForm()
    category = Category.objects.all()
    stil = CompetitionStil.objects.all()
    photo_form = PhotoForm()
    athletes = CompetitionsAthlete.objects.filter(competition=musabaka)

    if request.method == 'POST':


        #müsabaka link eklendi
        if request.POST.get('linkdefinition') and request.POST.get('linkyoutube'):
            link=Link(definition=request.POST.get('linkdefinition'),
                      youtubelink=request.POST.get('linkyoutube'))
            link.save()
            musabaka.youtubelink.add(link)
            musabaka.save()

        # döküman kaydedilecek alan
        if request.FILES.getlist('photofile') and request.POST.get('title'):
            files = request.FILES.getlist('photofile')
            date = request.POST.get('title')
            for item in files:
                photo = CompetitionPhotoDocumentDocument(title=date, file=item)
                photo.save()
                musabaka.photos.add(photo)
                musabaka.save()

        # döküman kaydedilecek alan
        if request.FILES.getlist('file') and request.POST.get('type'):
            files = request.FILES.getlist('file')
            type = request.POST.get('type')
            for item in files:
                dokuman = CompetitionsDocument(type=type,
                                               file=item)
                dokuman.save()
                musabaka.file.add(dokuman)
                musabaka.save()

        # form kaydedilme alani
        elif request.POST.get('name'):
            if competition_form.is_valid():

                for item in musabaka.stil.all():
                    musabaka.stil.remove(item)
                    musabaka.save()
                if request.POST.getlist('stil'):
                    for item in request.POST.getlist('stil'):
                        musabaka.stil.add(CompetitionStil.objects.get(pk=item))
                        musabaka.save()




                for item in musabaka.categoryies.all():
                    musabaka.categoryies.remove(item)
                    musabaka.save()
                if request.POST.getlist('jobDesription'):
                    for item in request.POST.getlist('jobDesription'):
                        musabaka.categoryies.add(Category.objects.get(pk=item))
                        musabaka.save()

                competition_form.save()
                messages.success(request, 'Müsabaka Başarıyla Güncellenmiştir.')

                log = str(request.POST.get('name')) + "  Musabaka guncellendi "
                log = general_methods.logwrite(request, request.user, log)

                return redirect('sbs:musabaka-duzenle', pk=pk)

            else:
                messages.warning(request, 'Alanları Kontrol Ediniz')
    competition_form = CompetitionForm(instance=musabaka)
    return render(request, 'musabaka/musabaka-duzenle.html',
                  {'competition_form': competition_form,
                   'competition': musabaka,
                   'athletes': athletes,
                   'category': category,
                   'stil': stil,
                   'photo_form': photo_form,
                   'dokuman_form': dokuman_form})


@login_required
def musabaka_sil(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Competition.objects.get(pk=pk)

            log = str(obj.name) + "  Musabaka silindi "
            log = general_methods.logwrite(request, request.user, log)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except Competition.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def musabaka_sporcu_ekle(request, athlete_pk, competition_pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST':
        compAthlete = CompetitionsAthlete()
        compAthlete.athlete = Athlete.objects.get(pk=athlete_pk)
        compAthlete.competition = Competition.objects.get(pk=competition_pk)
        compAthlete.save()
        messages.success(request, 'Sporcu Eklenmiştir')

    return redirect('sbs:lisans-listesi')


@login_required
def musabaka_sporcu_sec(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    category = Weight.objects.all().order_by('-weight')

    competition = Competition.objects.filter(registerStartDate__lte=timezone.now(),registerFinishDate__gte=timezone.now())

    return render(request, 'musabaka/musabaka-sporcu-sec.html',
                  {'pk': pk, 'weights': category, 'application': competition})


@login_required
def return_sporcu_ajax(request):
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        secilenler = request.GET.getlist('secilenler[]')
        pk = request.GET.get('athlete')
        athlete = Athlete.objects.get(pk=pk)

        # print('pk beklenen deger =',pk)
        # kategori = CompetitionCategori.objects.get(pk=request.GET.get('cmd'))

    elif request.method == 'POST':
        datatables = request.POST

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi

    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10
    modeldata = Athlete.objects.none()
    if length == -1:

        # athletes = []
        # for comp in compAthlete:
        #     if comp.athlete:
        #         athletes.append(comp.athlete.pk)
        modeldata = Athlete.objects.exclude(pk=athlete.pk)
        total = Athlete.objects.exclude(pk=athlete.pk).count()







    else:
        if search:
            modeldata = Athlete.objects.none()

            athletes = []
            modeldata = Athlete.objects.filter(
                Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                    user__email__icontains=search)).exclude(pk=athlete.pk)

            total = modeldata.count()


        else:
            modeldata = Athlete.objects.exclude(pk=athlete.pk)[start:start + length]
            total = Athlete.objects.exclude(pk=athlete.pk).distinct().count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []

    for item in modeldata:
        klup = ''
        try:
            if item.licenses:
                for lisans in item.licenses.all():
                    if lisans.sportsClub:
                        klup = str(lisans.sportsClub) + "<br>" + klup
        except:
            klup = ''
        if item.person.birthDate is not None:
            date = item.person.birthDate.strftime('%d/%m/%Y')
        else:
            date = ''
        data = {
            'id': 'row-' + str(item.pk),
            'say': say,
            'pk': item.pk,
            'tc': item.person.tc,
            'mail': item.user.email,
            'anne': item.person.motherName,
            'baba': item.person.fatherName,

            'name': item.user.first_name + ' ' + item.user.last_name,

            'birthDate': date,

            'klup': klup,

        }
        beka.append(data)
        say += 1

    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def return_sporcu(request):
    active = general_methods.controlGroup(request)
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        pk = request.GET.get('cmd')
        # print('pk beklenen deger =',pk)
        competition = Competition.objects.get(pk=pk)
        # kategori = CompetitionCategori.objects.get(pk=request.GET.get('cmd'))

    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10

    if length == -1:

        athletes = []
        for comp in CompetitionsAthlete.objects.filter(competition=competition):
            if comp.athlete:
                athletes.append(comp.athlete.pk)

        if active == 'KlupUye':
            sc_user = SportClubUser.objects.get(user=user)
            clubsPk = []
            clubs = SportsClub.objects.filter(clubUser=sc_user)
            for club in clubs:
                clubsPk.append(club.pk)

            modeldata = Athlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct()
            total = modeldata.count()

        elif active == 'Yonetim' or active == 'Admin':
            modeldata = Athlete.objects.exclude(pk__in=athletes)
            total = Athlete.objects.exclude(pk__in=athletes).count()

        elif active == 'Antrenor':
            modeldata = Athlete.objects.filter(licenses__coach__user=user).exclude(pk__in=athletes).distinct()[
                        start:start + length]

            total = Athlete.objects.filter(licenses__coach__user=user).exclude(pk__in=athletes).distinct().count()

    else:
        if search:
            modeldate = Athlete.objects.none()

            compAthlete = CompetitionsAthlete.objects.filter(competition=competition)
            athletes = []
            modeldata = Athlete.objects.filter(
                Q(user__last_name__icontains=search) | Q(user__first_name__icontains=search) | Q(
                    user__email__icontains=search))

            for comp in compAthlete:
                if comp.athlete:
                    athletes.append(comp.athlete.pk)
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                modeldata = modeldata.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct()
                total = modeldata.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct().count()
            elif active == 'Yonetim' or active == 'Admin':
                modeldata = modeldata.exclude(pk__in=athletes)


            elif active == 'Antrenor':
                modeldata = modeldata.filter(licenses__coach__user=user).distinct()

            total = modeldata.count()


        else:
            compAthlete = CompetitionsAthlete.objects.filter(competition=competition)
            athletes = []
            for comp in compAthlete:
                if comp.athlete:
                    athletes.append(comp.athlete.pk)
                    # print(comp.athlete)
            if active == 'KlupUye':
                sc_user = SportClubUser.objects.get(user=user)
                clubsPk = []
                clubs = SportsClub.objects.filter(clubUser=sc_user)
                for club in clubs:
                    clubsPk.append(club.pk)
                modeldata = Athlete.objects.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct()[start:start + length]
                total = Athlete.objects.exclude(pk__in=athletes).filter(
                    licenses__sportsClub__in=clubsPk).distinct().count()
            elif active == 'Yonetim' or active == 'Admin':
                modeldata = Athlete.objects.exclude(pk__in=athletes)[start:start + length]
                total = Athlete.objects.exclude(pk__in=athletes).distinct().count()


            elif active == 'Antrenor':
                modeldata = Athlete.objects.filter(licenses__coach__user=user).distinct()[
                            start:start + length]

                total = Athlete.objects.filter(licenses__coach__user=user).distinct().count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        klup = ''
        try:
            if item.licenses:
                for lisans in item.licenses.all():
                    if lisans.sportsClub:
                        klup = str(lisans.sportsClub) + "<br>" + klup
        except:
            klup = ''
        if item.person.birthDate is not None:
            date = item.person.birthDate.strftime('%d/%m/%Y')
        else:
            date = ''
        data = {
            'say': say,
            'pk': item.pk,

            'name': item.user.first_name + ' ' + item.user.last_name,

            'birthDate': date,

            'klup': klup,

        }
        beka.append(data)
        say += 1

    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def update_athlete(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            compAthlete = CompetitionsAthlete.objects.get(pk=competition)
            if Weight.objects.filter(pk=request.POST.get('category')):
                compAthlete.siklet = Weight.objects.get(pk=request.POST.get('category'))
            if Category.objects.filter(pk=request.POST.get('year')):
                compAthlete.category=Category.objects.get(pk=request.POST.get('year'))
            compAthlete.save()

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def choose_athlete_update(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:

            # bu alanda sporcu güncelleme alani olacak kategorisini güncelleme yapabilecegiz
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def choose_athlete(request, pk, competition):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            if request.POST.get('weight') and request.POST.get('category'):
                competition = Competition.objects.get(pk=competition)
                athlete = Athlete.objects.get(pk=pk)
                compAthlete = CompetitionsAthlete()
                if CompetitionsAthlete.objects.filter(competition=competition).filter(athlete=athlete).count() <= 1:
                    if CompetitionsAthlete.objects.filter(competition=competition).filter(athlete=athlete):
                        competitionAthlete = CompetitionsAthlete.objects.get(athlete=athlete, competition=competition)
                        competitionAthlete.siklet = Weight.objects.get(pk=request.POST.get('weight'))
                        competitionAthlete.category=Category.objects.get(pk=request.POST.get('category'))

                        competitionAthlete.save()
                        log = str(athlete.user.get_full_name()) + "  Musabakaya sporcu güncellendi "
                        log = general_methods.logwrite(request, request.user, log)
                        return JsonResponse({'status': 'Success', 'msg': 'Sporcu Başarı ile kaydedilmiştir.'})

                    else:
                        compAthlete.athlete = athlete
                        compAthlete.competition = competition
                        compAthlete.siklet = Weight.objects.get(pk=request.POST.get('weight'))
                        compAthlete.category = Category.objects.get(pk=request.POST.get('category'))
                        compAthlete.save()
                        log = str(athlete.user.get_full_name()) + "  Musabakaya sporcu eklendi "
                        log = general_methods.logwrite(request, request.user, log)
                        return JsonResponse({'status': 'Success', 'msg': 'Sporcu Başarı ile kaydedilmiştir.'})


                else:
                    return JsonResponse({'status': 'Fail', 'msg': 'Bir sporcu 3. defa eklenemez.'})

            else:
                return JsonResponse({'status': 'Fail', 'msg': 'Eksik'})


        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_sporcu_tamamla(request, athletes):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        athletes1 = request.POST.getlist('selected_options')
        if athletes1:
            return redirect('sbs:musabaka-sporcu-tamamla', athletes=athletes1)
            # for x in athletes1:
            #
            #         athlete = Athlete.objects.get(pk=x)
            #         compAthlete = CompAthlete()
            #         compAthlete.athlete = athlete
            #         compAthlete.competition = competition
            #         compAthlete.save()
        else:
            messages.warning(request, 'Sporcu Seçiniz')

    return render(request, 'musabaka/musabaka-sonuclar.html', {'athletes': athletes})


@login_required
def musabaka_sporcu_sil(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            athlete = CompetitionsAthlete.objects.get(pk=pk)

            log = str(athlete.athlete.user.get_full_name()) + "  müsabakadan silindi "
            log = general_methods.logwrite(request, request.user, log)

            athlete.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def result_list(request, pk):
    perm = general_methods.control_access_klup(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition = Competition.objects.filter(pk=pk)

    compAthlete = CompetitionsAthlete.objects.filter(competition=pk).order_by('degree')
    compCategory = CompCategory.objects.filter(competition=pk).order_by('-name')

    return render(request, 'musabaka/musabaka-sonuclar.html',
                  {'compCategory': compCategory, 'compAthlete': compAthlete})


@login_required
def return_competition_ajax(request):
    active = general_methods.controlGroup(request)
    # print('ben geldim')
    login_user = request.user
    user = User.objects.get(pk=login_user.pk)
    # /datatablesten gelen veri kümesi datatables degiskenine alindi
    if request.method == 'GET':
        datatables = request.GET
        pk = request.GET.get('cmd').strip()

    elif request.method == 'POST':
        datatables = request.POST
        # print(datatables)
        # print("post islemi gerceklesti")

    # /Sayfanın baska bir yerden istenmesi durumunda degerlerin None dönmemesi icin degerler try boklari icerisine alindi
    try:
        draw = int(datatables.get('draw'))
        # print("draw degeri =", draw)
        # Ambil start
        start = int(datatables.get('start'))
        # print("start degeri =", start)
        # Ambil length (limit)
        length = int(datatables.get('length'))
        # print("lenght  degeri =", length)
        # Ambil data search
        search = datatables.get('search[value]')
        # print("search degeri =", search)
    except:
        draw = 1
        start = 0
        length = 10
    modeldata = Competition.objects.none()
    if length == -1:
        print()

        # if user.groups.filter(name='KulupUye'):
        #     sc_user = SportClubUser.objects.get(user=user)
        #     clubsPk = []
        #     clubs = SportsClub.objects.filter(clubUser=sc_user)
        #     for club in clubs:
        #         clubsPk.append(club.pk)
        #
        #     modeldata = Athlete.objects.filter(licenses__sportsClub__in=clubsPk).distinct()
        #     total = modeldata.count()
        #
        # elif user.groups.filter(name__in=['Yonetim', 'Admin']):
        #     modeldata = Athlete.objects.all()
        #     total = Athlete.objects.all().count()


    else:
        if search:
            modeldata = Competition.objects.filter(
                Q(name=search))
            total = modeldata.count();

        else:
            # compAthlete=CompAthlete.objects.filter(competition=competition)
            # athletes = []
            # for comp in compAthlete:
            #     if comp.athlete:
            #             athletes.append(comp.athlete.pk)
            if active == 'KlupUye':
                # bu alan kontrol edilecek
                modeldata = Competition.objects.filter(year=pk)
                total = modeldata.count()
                # print('klüp üye ')
                # sc_user = SportClubUser.objects.get(user=user)
                # clubsPk = []
                # clubs = SportsClub.objects.filter(clubUser=sc_user)
                # for club in clubs:
                #     clubsPk.append(club.pk)
                # modeldata = Athlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct()[start:start + length]
                # total = mAthlete.objects.exclude(pk__in=athletes).filter(licenses__sportsClub__in=clubsPk).distinct().count()


            elif active == 'Yonetim' or active == 'Admin':

                modeldata = Competition.objects.filter(year=pk)
                total = modeldata.count()

    say = start + 1
    start = start + length
    page = start / length

    beka = []
    for item in modeldata:
        data = {
            'say': say,
            'pk': item.pk,
            'name': item.name,

        }
        beka.append(data)
        say += 1

    response = {

        'data': beka,
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,

    }
    return JsonResponse(response)


@login_required
def upload(request, pk):
    if Competition.objects.filter(pk=pk):
        competition = Competition.objects.filter(pk=pk)[0]
    else:
        return redirect('sbs:musabakalar')
    # if request.method == "POST":

    # excel_file = request.FILES["file"]
    # data = None
    # if (str(excel_file).split('.')[-1] == "xls"):
    #     data = xls_get(excel_file)
    #
    # elif (str(excel_file).split('.')[-1] == "xlsx"):
    #     data = xlsx_get(excel_file)
    # else:
    #     messages.warning(request, 'Lütfen bir excel dosyasi seçiniz (.xls -.xlsx)')
    #
    # if data:
    #     for item in data.items():
    #         count = 0
    #         for count in range(len(item[1])):
    #             # bir row alınmıs oldu
    #             print(item[1][count][0])
    #         print(len(item[1]))

    return render(request, 'musabaka/SonucAktar.html', {'competition': competition})


@login_required
def antrenor_ajax(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        beka = []
        for item in Coach.objects.all():
            data = {
                'pk': item.pk,
                'name': item.user.get_full_name(),
            }
            beka.append(data)
        return JsonResponse({'data': beka})
        # return HttpResponse(serializers.serialize("json", Coach.objects.all()))
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def antrenor_sporcu_ajax(request):
    perm = general_methods.control_access_klup(request)
    login_user = request.user

    if not perm:
        logout(request)
        return redirect('accounts:login')

    if request.method == 'POST' and request.is_ajax():
        if request.POST.get('coach'):
            coach = request.POST.get('coach')

            beka = []
            # antrenor verisi alınıp sistemde filtreleme yapılacak
            for item in Athlete.objects.filter(licenses__coach=Coach.objects.filter(pk=coach)[0]):
                data = {
                    'pk': item.pk,
                    'name': item.user.get_full_name(),
                }
                beka.append(data)
            return JsonResponse({'data': beka})

        # return HttpResponse(serializers.serialize("json", Coach.objects.all()))
    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_dokuman_sil(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            dokuman = CompetitionsDocument.objects.get(pk=pk)

            log = str(dokuman.file) + "  döküman silindi "
            log = general_methods.logwrite(request, request.user, log)

            dokuman.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def musabaka_photo_sil(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            dokuman = CompetitionPhotoDocumentDocument.objects.get(pk=pk)

            log = str(dokuman.title) + "  resim silindi "
            log = general_methods.logwrite(request, request.user, log)

            dokuman.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def musabaka_link_update(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            link = Link.objects.get(pk=pk)

            if request.POST.get('defi'):
                link.definition=request.POST.get('defi')
            if request.POST.get('link'):
                link.youtubelink=request.POST.get('link')
            link.save()
            log = str( pk)+ "  link güncellendi"
            log = general_methods.logwrite(request, request.user, log)
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def musabaka_link_delete(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():



        try:
            competition = Competition.objects.get(pk=pk)
            if Link.objects.filter(pk=request.POST.get('pk')):
                link = Link.objects.get(pk=request.POST.get('pk'))
                log = str(competition.name) + "  müsabasından" + link.youtubelink + "  linki silindi "
                log = general_methods.logwrite(request, request.user, log)
                competition.youtubelink.remove(link)
                competition.save()
                link.delete()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def choose_referee(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition = Competition.objects.get(pk=pk)
    competitionRole=JudgeRole.objects.all()
    if request.method == 'POST':
        if request.POST.get('judge') and  request.POST.get('role'):
            if Judge.objects.filter(pk=request.POST.get('judge')) and JudgeRole.objects.filter(pk=request.POST.get('role')):
                judge=Judge.objects.get(pk=request.POST.get('judge'))
                role=JudgeRole.objects.get(pk=request.POST.get('role'))
                rol=CompetitionJudgeRole(
                    judge=judge,
                    role=role
                )
                rol.save()
                competition.judges.add(rol)
                competition.save()

                # mail gönderiliyor

                log = str(judge.user.get_full_name()) + " Hakem "+competition.name+" müsabasına  eklendi"
                log = general_methods.logwrite(request, request.user, log)

                html_content = ''
                subject, from_email, to = 'Güreş Bilgi Sistemi Kullanıcı Bilgileri', 'no-reply@tgf.gov.tr', judge.user.email
                html_content = '<h2>TÜRKİYE GÜREŞ FEDERASYONU BİLGİ SİSTEMİ</h2>'
                html_content +=str(competition.name)+"müsabakasına      "+str(rol.role)+"      olarak eklendiniz."
                msg = EmailMultiAlternatives(subject, '', from_email, [to])
                msg.attach_alternative(html_content, "text/html")
                msg.send()

    coa = []
    for item in competition.judges.all():
        coa.append(item.judge.user.id)

    athletes = Judge.objects.exclude(user__in=coa)
        # return redirect('sbs:musabaka-duzenle', pk=pk)
    return render(request, 'musabaka/musabaka-hakem-sec.html', {
        'athletes': athletes,
        'competitionRole':competitionRole,
        'competition':competition
    })





@login_required
def choose_referee_ajax(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():



        try:
            competition = Competition.objects.get(pk=pk)
            print('ben geldim')

            # if Link.objects.filter(pk=request.POST.get('pk')):
            #
            #     return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})



@login_required
def musabaka_hakem_delete(request, pk):
    perm = general_methods.control_access_klup(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():



        try:
            competition = Competition.objects.get(pk=pk)
            if CompetitionJudgeRole.objects.filter(pk=request.POST.get('pk')):
                role = CompetitionJudgeRole.objects.get(pk=request.POST.get('pk'))
                log = str(competition.name) + "  müsabasından" + role.judge.user.get_full_name() + "  hakem  silindi "
                log = general_methods.logwrite(request, request.user, log)
                competition.judges.remove(role)
                competition.save()
                return JsonResponse({'status': 'Success', 'messages': 'save successfully'})

            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except SandaAthlete.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})

@login_required
def musabaka_rapor(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    competition = Competition.objects.get(pk=pk)
    compathlete=CompetitionsAthlete.objects.none()
    weight=Weight.objects.all()
    user_form = UserSearchForm()
    if request.method == 'POST':
        user_form = UserSearchForm(request.POST)
        firstName = unicode_tr(request.POST.get('first_name')).upper()
        lastName = unicode_tr(request.POST.get('last_name')).upper()
        email = request.POST.get('email')
        category = request.POST.get('category')
        siklet=request.POST.get('siklet')
        if not (firstName or lastName or email or category or siklet):
            compathlete = CompetitionsAthlete.objects.filter(competition=competition)
        else:
            query = Q()
            if lastName:
                query &= Q(last_name__icontains=lastName)
            if firstName:
                query &= Q(first_name__icontains=firstName)
            if email:
                query &= Q(email__icontains=email)
            if siklet:
                query &= Q(siklet_id=siklet)
            if category:
                query &= Q(category_id=category)
            compathlete = CompetitionsAthlete.objects.filter(competition=competition).filter(query)

    return render(request, 'musabaka/musabaka-basvuru-raporu.html', {
        'referees':compathlete,
        'competition':competition,
        'user_form':user_form,
        'weight':weight
    })
