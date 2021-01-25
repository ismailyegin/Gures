from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render

from sbs.Forms.ProductForm import ProductForm
from sbs.Forms.DepositForm import DepositForm
from sbs.models.Deposit import Deposit
from sbs.models.Products import Products
from sbs.services import general_methods



#
@login_required
def add_product(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product_form = ProductForm()
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Ürün  Başarıyla Eklenmiştir.')
            return redirect('sbs:urunler')
    return render(request, 'product/urunEkle.html', {'product_form': product_form})


@login_required
def return_products(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # comquery = CompetitionSearchForm()
    products = Products.objects.all()

    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     startDate = request.POST.get('startDate')
    #     compType = request.POST.get('compType')
    #     compGeneralType = request.POST.get('compGeneralType')
    #     if name or startDate or compType or compGeneralType:
    #         query = Q()
    #         if name:
    #             query &= Q(name__icontains=name)
    #         if startDate:
    #             query &= Q(startDate__year=int(startDate))
    #         if compType:
    #             query &= Q(compType__in=compType)
    #         if compGeneralType:
    #             query &= Q(compGeneralType__in=compGeneralType)
    #         activity = Activity.objects.filter(query).distinct()
    #     else:
    #         activity = Activity.objects.all()
    return render(request, 'product/urunler.html', {'products': products})


@login_required
def product_delete(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():


        try:
            obj = Products.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def product_update(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product = Products.objects.get(pk=pk)
    product_form = ProductForm(request.POST or None, instance=product)
    if request.method == 'POST':

        if product_form.is_valid():
            product_form.save()

            log = str(request.POST.get('name')) + " ürün guncelledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Ürün  Başarıyla Güncellenmiştir.')

            return redirect('sbs:urunler')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'product/urunDuzenle.html',
                  {'product_form': product_form})


@login_required
def add_product_deposit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product_form = DepositForm()
    if request.method == 'POST':
        product_form = DepositForm(request.POST)
        if product_form.is_valid():
            product_form.save()
            messages.success(request, 'Emanet   Başarıyla Eklenmiştir.')
            return redirect('sbs:urunler-emanet')
    return render(request, 'product/emanetEkle.html', {'product_form': product_form})


@login_required
def return_products_deposit(request):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    # comquery = CompetitionSearchForm()
    products = Deposit.objects.all()

    # if request.method == 'POST':
    #     name = request.POST.get('name')
    #     startDate = request.POST.get('startDate')
    #     compType = request.POST.get('compType')
    #     compGeneralType = request.POST.get('compGeneralType')
    #     if name or startDate or compType or compGeneralType:
    #         query = Q()
    #         if name:
    #             query &= Q(name__icontains=name)
    #         if startDate:
    #             query &= Q(startDate__year=int(startDate))
    #         if compType:
    #             query &= Q(compType__in=compType)
    #         if compGeneralType:
    #             query &= Q(compGeneralType__in=compGeneralType)
    #         activity = Activity.objects.filter(query).distinct()
    #     else:
    #         activity = Activity.objects.all()
    return render(request, 'product/emanetler.html', {'products': products})


@login_required
def product_delete_deposit(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')
    if request.method == 'POST' and request.is_ajax():

        try:
            obj = Deposit.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'status': 'Success', 'messages': 'save successfully'})
        except:
            return JsonResponse({'status': 'Fail', 'msg': 'Object does not exist'})

    else:
        return JsonResponse({'status': 'Fail', 'msg': 'Not a valid request'})


@login_required
def product_update_deposit(request, pk):
    perm = general_methods.control_access(request)

    if not perm:
        logout(request)
        return redirect('accounts:login')

    product = Deposit.objects.get(pk=pk)
    product_form = DepositForm(request.POST or None, instance=product)
    if request.method == 'POST':

        if product_form.is_valid():
            product_form.save()

            log = str(request.POST.get('name')) + " ürün emanet  guncelledi"
            log = general_methods.logwrite(request, request.user, log)

            messages.success(request, 'Ürün  Başarıyla Güncellenmiştir.')

            return redirect('sbs:urunler-emanet')
        else:

            messages.warning(request, 'Alanları Kontrol Ediniz')

    return render(request, 'product/emanetDuzenle.html',
                  {'product_form': product_form})
