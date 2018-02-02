import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect

from ABC.forms import OrderForm
from ABC.models import Order, OrderDetail, Item


@login_required
def new_order(request, order_id=None):
    if order_id:
        order = Order.objects.get(pk=order_id)
        form = OrderForm(instance=order)
    else:
        form = OrderForm()

    context = {'form': form, 'order_id': order_id}
    return render(request, 'ABC/new_order.html', context)


@login_required
def orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'ABC/orders.html', context)


@login_required
def add_order(request):
    if request.method == 'POST':
        # Add a new order in complete mode (with every field filled)
        form = OrderForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_order.html', {'form': form})
        order = Order()
        order.number = form.cleaned_data['number']
        order.date = form.cleaned_data['date']
        order.delivery_date = form.cleaned_data['delivery_date']
        order.state = form.cleaned_data['state']
        order.notes = form.cleaned_data['notes']
        order.customer = form.cleaned_data['customer']
        order.document = form.cleaned_data['document']
        order.delivery_type = form.cleaned_data['delivery_type']
        order.payment_type = form.cleaned_data['payment_type']
        order.finished = False
        order.payment_cost = order.payment_type.cost
        try:
            order.delivery_days = order.delivery_type.days
            order.delivery_cost = order.delivery_type.cost
        except:
            pass
        order.save()

        quantities = request.POST.getlist('quantity')
        prices = request.POST.getlist('retail_price')
        items = request.POST.getlist('items')

        i = 0
        tax_base = 0
        for item_id in items:
            item = Item.objects.get(pk=item_id)
            order_detail = OrderDetail()
            order_detail.order = order
            order_detail.item = item
            order_detail.discount = 0
            order_detail.subtotal = float(prices[i]) * int(quantities[i])
            order_detail.price = prices[i]
            order_detail.quantity = quantities[i]
            order_detail.save()
            tax_base += float(prices[i]) * int(quantities[i])
            i += 1

        order.tax_base = tax_base
        order.vat = order.tax_base * item.vat_type.rate / 100
        order.amount = tax_base + order.vat
        order.save()

        messages.success(request, 'Order created successfully')
        return redirect('new_order')


@login_required
def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('orders')


@login_required
def modify_order(request):
    if request.method == 'POST':
        order_id = request.POST['order_id']
        order = Order.objects.get(pk=order_id)
        # Modifiy a Order
        form = OrderForm(request.POST, request.FILES, instance=order)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_order.html', {'form': form, 'order_id': order_id})

        form.save()
        return redirect('orders')


@login_required
def order_details_info(request):
    order_number = request.GET.get('order_number')
    order_details = OrderDetail.objects.filter(order__number=order_number)
    order_details_json = {}

    for order_detail in order_details:
        details = {}
        details['quantity'] = order_detail.quantity
        details['retail_price'] = order_detail.price
        details['subtotal'] = order_detail.subtotal
        order_details_json[order_detail.item.name] = details

    data = json.dumps(order_details_json)
    return HttpResponse(data, 'application/json')


@login_required
def order_info(request):
    order_number = request.GET.get('order_number')
    order = Order.objects.get(number=order_number)
    order_json = {}

    order_json['company_name'] = order.customer.company_name
    order_json['date'] = order.date.strftime("%d/%m/%Y")
    order_json['state'] = order.state
    order_json['tax_base'] = order.tax_base
    order_json['vat'] = order.vat
    order_json['amount'] = order.amount
    order_json['finished'] = order.finished

    data = json.dumps(order_json)
    return HttpResponse(data, 'application/json')
