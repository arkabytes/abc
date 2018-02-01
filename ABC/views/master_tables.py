import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ABC.forms import VatTypeForm, PaymentTypeForm, DeliveryTypeForm
from ABC.models import VatType, PaymentType, DeliveryType


@login_required
def master_tables(request):
    vat_types = VatType.objects.all();
    delivery_types = DeliveryType.objects.all();
    payment_types = PaymentType.objects.all();
    context = {'vat_types': vat_types, 'delivery_types': delivery_types, 'payment_types': payment_types}
    return render(request, 'ABC/master_tables.html', context)


@login_required
def new_delivery_type(request, delivery_type_id=None):
    if delivery_type_id:
        delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
        form = DeliveryTypeForm(instance=delivery_type)
    else:
        form = DeliveryTypeForm()

    context = {'form': form, 'delivery_type_id': delivery_type_id}
    return render(request, 'ABC/new_delivery_type.html', context)


@login_required
def add_delivery_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = DeliveryTypeForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_delivery_type.html', {'form': form})

        form.save()
        messages.success(request, 'Delivery Type created successfully')
        return redirect('new_delivery_type')


@login_required
def delete_delivery_type(request, delivery_type_id):
    delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
    delivery_type.delete()
    return redirect('master_tables')


@login_required
def modify_delivery_type(request):
    if request.method == 'POST':
        delivery_type_id = request.POST['delivery_type_id']
        delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
        # Modify a Delivery Type
        form = DeliveryTypeForm(request.POST, request.FILES, instance=delivery_type)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_delivery_type.html', {'form': form, 'delivery_type_id': delivery_type_id})

        form.save()
        messages.success(request, 'Delivery Type modified successfully')
        return redirect('master_tables')


@login_required
def delivery_type_info(request):
    delivery_type_id = request.GET.get('delivery_type_id')
    delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
    delivery_type_json = {}
    delivery_type_json['name'] = delivery_type.name
    delivery_type_json['cost'] = delivery_type.cost

    data = json.dumps(delivery_type_json)
    return HttpResponse(data, 'application/json')


@login_required
def new_payment_type(request, payment_type_id=None):
    if payment_type_id:
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        form = PaymentTypeForm(instance=payment_type)
    else:
        form = PaymentTypeForm()

    context = {'form': form, 'payment_type_id': payment_type_id}
    return render(request, 'ABC/new_payment_type.html', context)


@login_required
def add_payment_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = PaymentTypeForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_payment_type.html', {'form': form})

        form.save()
        messages.success(request, 'Payment Type created successfully')
        return redirect('new_payment_type')


@login_required
def delete_payment_type(request, payment_type_id):
    payment_type = PaymentType.objects.get(pk=payment_type_id)
    payment_type.delete()
    return redirect('master_tables')


@login_required
def modify_payment_type(request):
    if request.method == 'POST':
        payment_type_id = request.POST['payment_type_id']
        payment_type = PaymentType.objects.get(pk=payment_type_id)
        # Modify a Payment Type
        form = PaymentTypeForm(request.POST, request.FILES, instance=payment_type)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_payment_type.html', {'form': form, 'payment_type_id': payment_type_id})

        form.save()
        messages.success(request, 'Payment Type modified successfully')
        return redirect('master_tables')


@login_required
def new_vat_type(request, vat_type_id=None):
    if vat_type_id:
        vat_type = VatType.objects.get(pk=vat_type_id)
        form = VatTypeForm(instance=vat_type)
    else:
        form = VatTypeForm()

    context = {'form': form, 'vat_type_id': vat_type_id}
    return render(request, 'ABC/new_vat_type.html', context)


@login_required
def add_vat_type(request):
    if request.method == 'POST':
        # Add a new VAT Type
        form = VatTypeForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_vat_type.html', {'form': form})

        form.save()
        messages.success(request, 'Vat Type created successfully')
        return redirect('new_vat_type')


@login_required
def delete_vat_type(request, vat_type_id):
    vat_type = VatType.objects.get(pk=vat_type_id)
    vat_type.delete()
    return redirect('master_tables')


@login_required
def modify_vat_type(request):
    if request.method == 'POST':
        vat_type_id = request.POST['vat_type_id']
        vat_type = VatType.objects.get(pk=vat_type_id)
        # Modifiy a VAT Type
        form = VatTypeForm(request.POST, request.FILES, instance=vat_type)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_vat_type.html', {'form': form, 'vat_type_id': vat_type_id})

        form.save()
        messages.success(request, 'Vat Type modified successfully')
        return redirect('master_tables')
