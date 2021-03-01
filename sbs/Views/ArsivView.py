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
from sbs.models.EnumFields import EnumFields
from sbs.services import general_methods
from sbs.Forms.SimplecategoryForm import SimplecategoryForm
from sbs.models.Activity import Activity
from sbs.Forms.ActivityForm import ActivityForm

from sbs.models.Abirim import Abirim
from sbs.Forms.AbirimForm import AbirimForm

from datetime import date, datetime
from django.utils import timezone

from sbs.Forms.AcategoriForm import AcategoriForm
from sbs.models.CategoryItem import CategoryItem

from sbs.models.AbirimParametre import AbirimParametre
from sbs.Forms.AbirimparametreFrom import AbirimparametreForm

from sbs.models.Aklasor import Aklasor
from sbs.Forms.AklasorForm import AklasorForm

from sbs.models.Adosya import Adosya
from sbs.Forms.AdosyaForm import AdosyaForm

from sbs.models.AdosyaParametre import AdosyaParametre
from sbs.Forms.AdosyaparametreForm import AdosyaparametreForm

from sbs.models.Aevrak import Aevrak
from sbs.Forms.AevrakForm import AevrakForm


@login_required
def return_arsiv(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    return render(request, 'arsiv/arsiv.html')


@login_required
def arsiv_location_add(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        category_item_form = AcategoriForm(request.POST)
        if category_item_form.is_valid():
            categori = category_item_form.save(commit=False)
            categori.forWhichClazz = "location"
            categori.save()
    category_item_form = AcategoriForm()
    categoryitem = CategoryItem.objects.filter(forWhichClazz='location')
    return render(request, 'arsiv/location.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def arsiv_location_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    categori = CategoryItem.objects.get(pk=pk)
    category_item_form = AcategoriForm(request.POST or None, instance=categori)
    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
            return redirect('sbs:arsiv-konumEkle')
    categoryitem = CategoryItem.objects.filter(forWhichClazz='location')

    return render(request, 'arsiv/location.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def arsiv_birim_add(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST':
        category_item_form = AbirimForm(request.POST)
        if category_item_form.is_valid():
            category_item_form.save()

    category_item_form = AbirimForm()
    categoryitem = Abirim.objects.all()
    return render(request, 'arsiv/birimAdd.html',
                  {'category_item_form': category_item_form, 'categoryitem': categoryitem})


@login_required
def categoryItemDelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = Abirim.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def arsiv_birim_update(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    birim = Abirim.objects.get(pk=pk)
    category_item_form = AbirimForm(request.POST or None, instance=birim)

    if request.method == 'POST':
        if category_item_form.is_valid():
            category_item_form.save()
    categoryitem = AbirimParametre.objects.filter(birim=birim)
    return render(request, 'arsiv/birimGuncelle.html', {'category_item_form': category_item_form,
                                                        'categoryitem': categoryitem,
                                                        'birim': birim})


@login_required
def arsiv_birimParametre(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    abirim = Abirim.objects.get(pk=pk)
    category_item_form = AbirimparametreForm(request.POST or None)
    if request.method == 'POST':
        if category_item_form.is_valid():
            test = AbirimParametre(title=category_item_form.cleaned_data['title'],
                                   birim=abirim,
                                   type=category_item_form.cleaned_data['type']
                                   )
            test.save()
            print()
            print(test.birim.name)
            print(test)

            return redirect('sbs:arsiv-birimUpdate', pk=abirim.pk)

    return render(request, 'arsiv/parametreEkle.html', {'parametre_form': category_item_form, })


@login_required
def arsiv_birimParametreUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    parametre = AbirimParametre.objects.get(pk=pk)
    category_item_form = AbirimparametreForm(request.POST or None, instance=parametre)

    if request.method == 'POST':
        if category_item_form.is_valid():
            test = category_item_form.save()
            test.save()
            return redirect('sbs:arsiv-birimUpdate', parametre.birim.pk)

    return render(request, 'arsiv/parametreEkle.html', {'parametre_form': category_item_form, })


@login_required
def arsiv_birimListesi(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    birimler = []
    categori = Abirim.objects.all()

    for item in categori:
        parametre = AbirimParametre.objects.filter(birim=item)
        # print(parametre.values_list("title","title"))
        beka = {
            'pk': item.pk,
            'name': item.name,
            'parametre': parametre
        }
        birimler.append(beka)

    # arama alani yazılacak
    # if request.method == 'POST':
    #     if category_item_form.is_valid():
    #         category_item_form.save()
    #         return redirect('sbs:arsiv-birimEkle')

    return render(request, 'arsiv/BirimList.html', {'birimler': birimler})


@login_required
def parametredelete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():
        try:
            obj = AbirimParametre.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except CategoryItem.DoesNotExist:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


def arsiv_klasorEkle(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    form = AklasorForm()
    if request.method == 'POST':
        form = AklasorForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.save()

            return redirect('sbs:klasor-guncelle', form.pk)

    return render(request, 'arsiv/KlasorEkle.html', {'form': form})


def arsiv_klasorler(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    birimler = []
    klasor = Aklasor.objects.all()

    for item in klasor:
        parametre = Adosya.objects.filter(klasor=item)
        # print(parametre.values_list("title","title"))
        beka = {
            'pk': item.pk,
            'name': item.name,
            'parametre': parametre
        }
        birimler.append(beka)

    # arama alani yazılacak
    # if request.method == 'POST':
    #     if category_item_form.is_valid():
    #         category_item_form.save()
    #         return redirect('sbs:arsiv-birimEkle')

    return render(request, 'arsiv/KlasorListesi.html', {'birimler': birimler})


@login_required
def arsiv_klasorUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    klasor = Aklasor.objects.get(pk=pk)
    klasor_form = AklasorForm(request.POST or None, instance=klasor)
    dosya = Adosya.objects.filter(klasor=klasor)

    if request.method == 'POST':
        if klasor_form.is_valid():
            test = klasor_form.save()
            test.save()

    return render(request, 'arsiv/KlasorGuncelle.html', {'form': klasor_form, 'dosya': dosya, 'klasor': klasor})


def arsiv_dosyaEkle(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    klasor = Aklasor.objects.get(pk=pk)
    birim = klasor.birim
    form = AdosyaForm(klasor, birim)

    formparametre = AdosyaparametreForm()

    if request.method == 'POST':
        form = AdosyaForm(klasor, birim, request.POST)
        formparametre = AdosyaparametreForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sbs:klasor-guncelle', pk)

    return render(request, 'arsiv/DosyaEkle.html', {'form': form})


@login_required
def arsiv_dosyaUpdate(request, pk):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')
    dosya = Adosya.objects.get(pk=pk)
    form = AdosyaForm(request.POST or None, instance=dosya)
    parametre = AdosyaParametre.objects.filter(dosya=dosya)
    print(parametre)
    if request.method == 'POST':
        if form.is_valid():
            test = form.save(commit=False)
            test.save()
            return redirect('sbs:klasor-guncelle', dosya.klasor.pk)
    return render(request, 'arsiv/DosyaGuncelle.html', {'form': form, 'dosya': dosya, 'parametre': parametre})


@login_required
def arsiv_evrakEkle(request):
    perm = general_methods.control_access(request)
    if not perm:
        logout(request)
        return redirect('accounts:login')

    form = AevrakForm(3)
    if request.method == 'POST':
        form = AevrakForm(3, request.POST)
        if form.is_valid():
            form.save()
            # return redirect('sbs:klasor-guncelle', dosya.klasor.pk)

    return render(request, 'arsiv/EvrakEkle.html',
                  {'form': form, }
                  )
