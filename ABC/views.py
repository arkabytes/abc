from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from reportlab.pdfgen import canvas
from io import BytesIO
import json

from ABC.models import Item, Customer, Provider, VatType, PaymentType, DeliveryType
from arkaABC.settings import ITEMS_PER_PAGE
from .forms import ItemQuickForm, ItemForm
from .forms import CustomerQuickForm, CustomerForm, VatTypeForm, PaymentTypeForm, DeliveryTypeForm, ProviderForm, ProviderQuickForm


def index(request):
    if request.user.is_authenticated:
        return render(request, 'ABC/index.html')
    else:
        return redirect('signin')


def signin(request):
    return render(request, 'ABC/signin.html')


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('index')

    context = {'message': 'Invalid Username/Password'}
    # I should invoke directly to the view with the context
    return render(request, 'ABC/signin.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def item(request, item_id):
    the_item = Item.objects.get(id=item_id)
    context = {'the_item': the_item}
    return render(request, 'ABC/item.html', context)


def new_item(request):
    return render(request, 'ABC/new_item.html')


def add_item(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new item in quick mode
            form = ItemQuickForm(request.POST, request.FILES)
            if form.is_valid():
                the_item = Item()
                the_item.name = form.cleaned_data['name']
                the_item.description = form.cleaned_data['description']
                the_item.retail_price = form.cleaned_data['retail_price']
                the_item.thumbnail = form.cleaned_data['thumbnail']
                the_item.save()

            return HttpResponseRedirect(reverse('items'))
        else:
            # Add a new item in complete mode (with every field filled)
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                the_item = Item()
                the_item.name = form.cleaned_data['name']
                the_item.description = form.cleaned_data['description']
                the_item.notes = form.cleaned_data['notes']
                the_item.stock = form.cleaned_data['stock']
                the_item.cost_price = form.cleaned_data['cost_price']
                the_item.retail_price = form.cleaned_data['retail_price']
                the_item.thumbnail = form.cleaned_data['thumbnail']
                the_item.image1 = form.cleaned_data['image1']
                the_item.image2 = form.cleaned_data['image2']
                the_item.image3 = form.cleaned_data['image3']
                # the_item.provider =
                # the_item.vat_type =
                the_item.save()
            else:
                return render(request, 'ABC/new_item.html', {'form':form})

            return HttpResponseRedirect(reverse('new_item'))


def delete_item(request, item_id):
    an_item = Item.objects.get(id=item_id)
    an_item.delete()
    return HttpResponseRedirect(reverse('items'))


def items(request):
    all_items = Item.objects.order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(all_items, ITEMS_PER_PAGE)
    try:
        items = paginator.page(page)
    except PageNotAnInteger:
        items = paginator.page(1)
    except EmptyPage:
        items = paginator.page(paginator.num_pages)

    context = {'items': items}
    return render(request, 'ABC/items.html', context)


def autocomplete_item(request):
    data = request.GET
    content_data = data.get('term')
    if content_data:
        items = Item.objects.filter(name__contains=content_data)
    else:
        items = Item.objects.all()

    results = []
    for item in items:
        item_json = {}
        item_json['label'] = item.name
        item_json['id'] = item.id
        item_json['name'] = item.name
        item_json['description'] = item.description
        if item.stock > 0:
            item_json['availability'] = 'In Stock'
        else:
            item_json['availability'] = 'Out of Stock'
        item_json['retail_price'] = item.retail_price
        results.append(item_json)

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def customer(request, customer_id):
    the_customer = Item.objects.get(id=customer_id)
    context = {'the_customer': the_customer}
    return render(request, 'ABC/customer.html', context)


def new_customer(request):
    form = CustomerForm()
    return render(request, 'ABC/new_customer.html', {'form': form})


def add_customer(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new customer in quick mode
            form = CustomerQuickForm(request.POST, request.FILES)
            if form.is_valid():
                the_customer = Customer()
                the_customer.company_name = form.cleaned_data['company_name']
                the_customer.name = form.cleaned_data['name']
                the_customer.email = form.cleaned_data['email']
                the_customer.save()

            return HttpResponseRedirect(reverse('customers'))
        else:
            # Add a new customer in complete mode (with every field filled)
            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                the_customer = Customer()
                the_customer.cif = form.cleaned_data['cif']
                the_customer.company_name = form.cleaned_data['company_name']
                the_customer.name = form.cleaned_data['name']
                the_customer.surname = form.cleaned_data['surname']
                the_customer.address = form.cleaned_data['address']
                the_customer.city = form.cleaned_data['city']
                the_customer.province = form.cleaned_data['province']
                the_customer.postal_code = form.cleaned_data['postal_code']
                the_customer.country = form.cleaned_data['country']
                the_customer.phone = form.cleaned_data['phone']
                the_customer.fax = form.cleaned_data['fax']
                the_customer.email = form.cleaned_data['email']
                the_customer.web = form.cleaned_data['web']
                the_customer.notes = form.cleaned_data['notes']
                the_customer.save()
            else:
                return render(request, 'ABC/new_customer.html', {'form':form})

            return HttpResponseRedirect(reverse('new_customer'))


def delete_customer(request, customer_id):
    a_customer = Customer.objects.get(id=customer_id)
    a_customer.delete()
    return HttpResponseRedirect(reverse('customers'))


def report_customers(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customers.pdf"'

    buffer = BytesIO()

    can = canvas.Canvas(buffer)
    can.drawString(0, 0, "Customers")
    can.showPage()
    can.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


def customers(request):
    all_customers = Customer.objects.order_by('name')
    context = {'customers': all_customers}
    return render(request, 'ABC/customers.html', context)


def autocomplete_customer(request):
    content_data = request.GET.get('term')
    if content_data:
        customers = Customer.objects.filter(name__contains=content_data)
    else:
        customers = Customer.objects.all()

    results = []
    for customer in customers:
        customer_json = {}
        customer_json['label'] = customer.name
        customer_json['name'] = customer.name
        customer_json['company_name'] = customer.company_name
        results.append(customer_json)

    data = json.dumps(results)
    return HttpResponse(data, 'application/json')


def customer_info(request):

    customer_id = request.GET.get('customer_id')
    customer = Customer.objects.get(pk=customer_id)
    customer_json = {}
    customer_json['name'] = customer.name
    customer_json['company_name'] = customer.company_name
    customer_json['location'] = customer.city + ", " + customer.province
    customer_json['email'] = customer.email
    customer_json['web'] = customer.web

    data = json.dumps(customer_json)
    return HttpResponse(data, 'application/json')


def new_provider(request):
    return render(request, 'ABC/new_provider.html')


def add_provider(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new provider in quick mode
            form = ProviderQuickForm(request.POST, request.FILES)
            if form.is_valid():
                the_provider = Provider()
                the_provider.name = form.cleaned_data['name']
                the_provider.contact_name = form.cleaned_data['contact_name']
                the_provider.email = form.cleaned_data['email']
                the_provider.save()

            return HttpResponseRedirect(reverse('providers'))
        else:
            # Add a new provider in complete mode (with every field filled)
            form = ProviderForm(request.POST, request.FILES)
            if form.is_valid():
                the_provider = Provider()
                the_provider.cif = form.cleaned_data['cif']
                the_provider.name = form.cleaned_data['name']
                the_provider.contact_name = form.cleaned_data['contact_name']
                the_provider.address = form.cleaned_data['address']
                the_provider.city = form.cleaned_data['city']
                the_provider.province = form.cleaned_data['province']
                the_provider.postal_code = form.cleaned_data['postal_code']
                the_provider.country = form.cleaned_data['country']
                the_provider.phone = form.cleaned_data['phone']
                the_provider.fax = form.cleaned_data['fax']
                the_provider.email = form.cleaned_data['email']
                the_provider.web = form.cleaned_data['web']
                the_provider.notes = form.cleaned_data['notes']
                the_provider.save()
            else:
                print(form.errors)
                return render(request, 'ABC/new_provider.html', {'form':form})

            return HttpResponseRedirect(reverse('new_provider'))


def delete_provider(request, provider_id):
    a_provider = Provider.objects.get(id=provider_id)
    a_provider.delete()
    return HttpResponseRedirect(reverse('providers'))


def providers(request):
    providers = Provider.objects.all()
    context = {'providers': providers}
    return render(request, 'ABC/providers.html', context)


def new_order(request):
    return render(request, 'ABC/new_order.html')


def orders(request):
    return render(request, 'ABC/orders.html')


def add_order(request):
    pass;


def delete_order(request):
    pass;


def new_invoice(request):
    return render(request, 'ABC/new_invoice.html')


def invoices(request):
    return render(request, 'ABC/invoices.html')


def add_invoice(request):
    pass;


def delete_invoice(request):
    pass;


def new_event(request):
    return render(request, 'ABC/new_event.html')


def events(request):
    return render(request, 'ABC/events.html')


def add_event(request):
    pass;


def delete_event(request):
    pass;


def new_task(request):
    return render(request, 'ABC/new_task.html')


def tasks(request):
    return render(request, 'ABC/tasks.html')


def add_task(request):
    pass;


def delete_task(request):
    pass;


def master_tables(request):

    vat_types = VatType.objects.all();
    delivery_types = DeliveryType.objects.all();
    payment_types = PaymentType.objects.all();
    context = {'vat_types': vat_types, 'delivery_types': delivery_types, 'payment_types': payment_types}
    return render(request, 'ABC/master_tables.html', context)


def new_delivery_type(request):
    return render(request, 'ABC/new_delivery_type.html')


def add_delivery_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = DeliveryTypeForm(request.POST, request.FILES)
        if form.is_valid():
            the_delivery_type = DeliveryType()
            the_delivery_type.name = form.cleaned_data['name']
            the_delivery_type.description = form.cleaned_data['description']
            the_delivery_type.cost = form.cleaned_data['cost']
            the_delivery_type.days = form.cleaned_data['days']
            the_delivery_type.save()
        else:
            return render(request, 'ABC/new_delivery_type.html', {'form':form})

        return HttpResponseRedirect(reverse('new_delivery_type'))


def delete_delivery_type(request, delivery_type_id):
    delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
    delivery_type.delete()
    return redirect('master_tables')


def new_payment_type(request):
    return render(request, 'ABC/new_payment_type.html')


def add_payment_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = PaymentTypeForm(request.POST, request.FILES)
        if form.is_valid():
            the_payment_type = PaymentType()
            the_payment_type.name = form.cleaned_data['name']
            the_payment_type.description = form.cleaned_data['description']
            the_payment_type.cost = form.cleaned_data['cost']
            the_payment_type.save()
        else:
            return render(request, 'ABC/new_payment_type.html', {'form':form})

        return HttpResponseRedirect(reverse('new_payment_type'))


def delete_payment_type(request, payment_type_id):
    payment_type = PaymentType.objects.get(pk=payment_type_id)
    payment_type.delete()
    return redirect('master_tables')


def new_vat_type(request):
    return render(request, 'ABC/new_vat_type.html')


def add_vat_type(request):
    if request.method == 'POST':
        # Add a new VAT Type
        form = VatTypeForm(request.POST, request.FILES)
        if form.is_valid():
            the_vat_type = VatType()
            the_vat_type.name = form.cleaned_data['name']
            the_vat_type.rate = form.cleaned_data['rate']
            the_vat_type.save()
        else:
            return render(request, 'ABC/new_vat_type.html', {'form':form})

        return HttpResponseRedirect(reverse('new_vat_type'))


def delete_vat_type(request, vat_type_id):

    vat_type = VatType.objects.get(pk=vat_type_id)
    vat_type.delete()
    return redirect('master_tables')
