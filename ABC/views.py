from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from reportlab.pdfgen import canvas
from io import BytesIO
import json

from ABC.models import Item, Customer, Provider, VatType, PaymentType, DeliveryType
from ABC.models import Event, Task, Order, Invoice
from arkaABC.settings import ITEMS_PER_PAGE
from .forms import ItemQuickForm, ItemForm, OrderForm, InvoiceForm, TaskForm, EventForm, TaskQuickForm
from .forms import CustomerQuickForm, CustomerForm, VatTypeForm, PaymentTypeForm, DeliveryTypeForm, ProviderForm, ProviderQuickForm


def index(request):
    ##if request.user.is_authenticated:
    return render(request, 'ABC/index.html')
    ##else:
    ##    return redirect('signin')


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
    return redirect('index')


def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'the_item': item}
    return render(request, 'ABC/item.html', context)


def new_item(request):
    form = ItemForm()
    context = {'form': form}
    return render(request, 'ABC/new_item.html', context)


def add_item(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new item in quick mode
            form = ItemQuickForm(request.POST, request.FILES)
            if form.is_valid():
                item = Item()
                item.name = form.cleaned_data['name']
                item.description = form.cleaned_data['description']
                item.retail_price = form.cleaned_data['retail_price']
                item.thumbnail = form.cleaned_data['thumbnail']
                item.save()

            return redirect('items')
        else:
            # Add a new item in complete mode (with every field filled)
            form = ItemForm(request.POST, request.FILES)
            if form.is_valid():
                item = Item()
                item.name = form.cleaned_data['name']
                item.description = form.cleaned_data['description']
                item.notes = form.cleaned_data['notes']
                item.stock = form.cleaned_data['stock']
                item.cost_price = form.cleaned_data['cost_price']
                item.retail_price = form.cleaned_data['retail_price']
                item.thumbnail = form.cleaned_data['thumbnail']
                item.image1 = form.cleaned_data['image1']
                item.image2 = form.cleaned_data['image2']
                item.image3 = form.cleaned_data['image3']
                # item.provider =
                # item.vat_type =
                item.save()
            else:
                return render(request, 'ABC/new_item.html', {'form':form})

            return redirect('new_item')


def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('items')


def items(request):
    items = Item.objects.order_by('name')
    page = request.GET.get('page', 1)

    paginator = Paginator(items, ITEMS_PER_PAGE)
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
    customer = Customer.objects.get(id=customer_id)
    context = {'customer': customer}
    return render(request, 'ABC/customer.html', context)


def new_customer(request):
    form = CustomerForm()
    context = {'form': form}
    return render(request, 'ABC/new_customer.html', context)


def add_customer(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new customer in quick mode
            form = CustomerQuickForm(request.POST, request.FILES)
            if form.is_valid():
                customer = Customer()
                customer.company_name = form.cleaned_data['company_name']
                customer.name = form.cleaned_data['name']
                customer.email = form.cleaned_data['email']
                customer.save()

            return redirect('customers')
        else:
            # Add a new customer in complete mode (with every field filled)
            form = CustomerForm(request.POST, request.FILES)
            if form.is_valid():
                customer = Customer()
                customer.cif = form.cleaned_data['cif']
                customer.company_name = form.cleaned_data['company_name']
                customer.name = form.cleaned_data['name']
                customer.surname = form.cleaned_data['surname']
                customer.address = form.cleaned_data['address']
                customer.city = form.cleaned_data['city']
                customer.province = form.cleaned_data['province']
                customer.postal_code = form.cleaned_data['postal_code']
                customer.country = form.cleaned_data['country']
                customer.phone = form.cleaned_data['phone']
                customer.fax = form.cleaned_data['fax']
                customer.email = form.cleaned_data['email']
                customer.web = form.cleaned_data['web']
                customer.notes = form.cleaned_data['notes']
                customer.save()
            else:
                return render(request, 'ABC/new_customer.html', {'form':form})

            return redirect('new_customer')


def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('customers')


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
    customers = Customer.objects.order_by('name')
    context = {'customers': customers}
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
    form = ProviderForm()
    context = {'form': form}
    return render(request, 'ABC/new_provider.html', context)


def add_provider(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new provider in quick mode
            form = ProviderQuickForm(request.POST, request.FILES)
            if form.is_valid():
                provider = Provider()
                provider.name = form.cleaned_data['name']
                provider.contact_name = form.cleaned_data['contact_name']
                provider.email = form.cleaned_data['email']
                provider.save()

            return redirect('providers')
        else:
            # Add a new provider in complete mode (with every field filled)
            form = ProviderForm(request.POST, request.FILES)
            if form.is_valid():
                provider = Provider()
                provider.cif = form.cleaned_data['cif']
                provider.name = form.cleaned_data['name']
                provider.contact_name = form.cleaned_data['contact_name']
                provider.address = form.cleaned_data['address']
                provider.city = form.cleaned_data['city']
                provider.province = form.cleaned_data['province']
                provider.postal_code = form.cleaned_data['postal_code']
                provider.country = form.cleaned_data['country']
                provider.phone = form.cleaned_data['phone']
                provider.fax = form.cleaned_data['fax']
                provider.email = form.cleaned_data['email']
                provider.web = form.cleaned_data['web']
                provider.notes = form.cleaned_data['notes']
                provider.save()
            else:
                print(form.errors)
                return render(request, 'ABC/new_provider.html', {'form':form})

            return redirect('new_provider')


def delete_provider(request, provider_id):
    provider = Provider.objects.get(id=provider_id)
    provider.delete()
    return redirect('providers')


def providers(request):
    providers = Provider.objects.all()
    context = {'providers': providers}
    return render(request, 'ABC/providers.html', context)


def new_order(request):
    form = OrderForm()
    context = {'form': form}
    return render(request, 'ABC/new_order.html', context)


def orders(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, 'ABC/orders.html', context)


def add_order(request):
    pass;


def delete_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    order.delete()
    return redirect('orders')


def new_invoice(request):
    form = InvoiceForm()
    context = {'form': form}
    return render(request, 'ABC/new_invoice.html', context)


def invoices(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'ABC/invoices.html', context)


def add_invoice(request):
    pass;


def delete_invoice(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    invoice.delete()
    return redirect('invoices')


def new_event(request):
    form = EventForm()
    context = {'form': form}
    return render(request, 'ABC/new_event.html', context)


def events(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'ABC/events.html', context)


def add_event(request):
    if request.method == 'POST':
        # Add a new event in complete mode (with every field filled)
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = Event()
            event.name = form.cleaned_data['name']
            event.description = form.cleaned_data['description']
            event.date = form.cleaned_data['date']
            event.location = form.cleaned_data['location']
            event.customer = form.cleaned_data['customer']
            event.provider = form.cleaned_data['provider']
            event.notice_date = form.cleaned_data['notice_date']
            event.save()
        else:
            print(form.errors)
            return render(request, 'ABC/new_event.html', {'form':form})

    return redirect('new_event')

def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events')


def new_task(request):
    form = TaskForm()
    context = {'form': form}
    return render(request, 'ABC/new_task.html', context)


def tasks(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'ABC/tasks.html', context)


def add_task(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new task in quick mode
            form = TaskQuickForm(request.POST, request.FILES)
            if form.is_valid():
                task = Task()
                task.name = form.cleaned_data['name']
                task.description = form.cleaned_data['description']
                task.date = form.cleaned_data['date']
                task.save()

            return redirect('tasks')
        else:
            # Add a new task in complete mode (with every field filled)
            form = TaskForm(request.POST, request.FILES)
            if form.is_valid():
                task = Task()
                task.name = form.cleaned_data['name']
                task.description = form.cleaned_data['description']
                task.date = form.cleaned_data['date']
                task.start_date = form.cleaned_data['start_date']
                task.finish_date = form.cleaned_data['finish_date']
                task.location = form.cleaned_data['location']
                task.customer = form.cleaned_data['customer']
                task.provider = form.cleaned_data['provider']
                task.order = form.cleaned_data['order']
                task.state = form.cleaned_data['state']
                task.notice = form.cleaned_data['notice']
                task.notice_date = form.cleaned_data['notice_date']
                task.save()
            else:
                print(form.errors)
                return render(request, 'ABC/new_task.html', {'form':form})

        return redirect('new_task')


def delete_task(request, task_id):
    task = Task.objects.get(pk=task_id)
    task.delete()
    return redirect('tasks')


def master_tables(request):
    vat_types = VatType.objects.all();
    delivery_types = DeliveryType.objects.all();
    payment_types = PaymentType.objects.all();
    context = {'vat_types': vat_types, 'delivery_types': delivery_types, 'payment_types': payment_types}
    return render(request, 'ABC/master_tables.html', context)


def new_delivery_type(request):
    form = DeliveryTypeForm()
    context = {'form': form}
    return render(request, 'ABC/new_delivery_type.html', context)


def add_delivery_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = DeliveryTypeForm(request.POST, request.FILES)
        if form.is_valid():
            delivery_type = DeliveryType()
            delivery_type.name = form.cleaned_data['name']
            delivery_type.description = form.cleaned_data['description']
            delivery_type.cost = form.cleaned_data['cost']
            delivery_type.days = form.cleaned_data['days']
            delivery_type.save()
        else:
            form.errors
            return render(request, 'ABC/new_delivery_type.html', {'form':form})

        return redirect('new_delivery_type')


def delete_delivery_type(request, delivery_type_id):
    delivery_type = DeliveryType.objects.get(pk=delivery_type_id)
    delivery_type.delete()
    return redirect('master_tables')


def new_payment_type(request):
    form = PaymentTypeForm()
    context = {'form': form}
    return render(request, 'ABC/new_payment_type.html', context)


def add_payment_type(request):
    if request.method == 'POST':
        # Add a new Payment Type
        form = PaymentTypeForm(request.POST, request.FILES)
        if form.is_valid():
            payment_type = PaymentType()
            payment_type.name = form.cleaned_data['name']
            payment_type.description = form.cleaned_data['description']
            payment_type.cost = form.cleaned_data['cost']
            payment_type.save()
        else:
            return render(request, 'ABC/new_payment_type.html', {'form':form})

        return redirect('new_payment_type')


def delete_payment_type(request, payment_type_id):
    payment_type = PaymentType.objects.get(pk=payment_type_id)
    payment_type.delete()
    return redirect('master_tables')


def new_vat_type(request):
    form = VatTypeForm()
    context = {'form': form}
    return render(request, 'ABC/new_vat_type.html', context)


def add_vat_type(request):
    if request.method == 'POST':
        # Add a new VAT Type
        form = VatTypeForm(request.POST, request.FILES)
        if form.is_valid():
            vat_type = VatType()
            vat_type.name = form.cleaned_data['name']
            vat_type.rate = form.cleaned_data['rate']
            vat_type.save()
        else:
            return render(request, 'ABC/new_vat_type.html', {'form':form})

        return redirect('new_vat_type')


def delete_vat_type(request, vat_type_id):
    vat_type = VatType.objects.get(pk=vat_type_id)
    vat_type.delete()
    return redirect('master_tables')
