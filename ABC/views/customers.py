import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

from ABC.forms import CustomerForm, CustomerQuickForm
from ABC.models import Customer


@login_required
def customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    context = {'customer': customer}
    return render(request, 'ABC/customer.html', context)


@login_required
def new_customer(request, customer_id=None):
    if customer_id:
        customer = Customer.objects.get(pk=customer_id)
        form = CustomerForm(instance=customer)
    else:
        form = CustomerForm()

    context = {'form': form, 'customer_id': customer_id}
    view = request.GET.get('view')
    if view == '1':
        context['view'] = True

    return render(request, 'ABC/new_customer.html', context)


@login_required
def add_customer(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new customer in quick mode
            form = CustomerQuickForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return redirect('customers')

            form.save()
            messages.success(request, 'Customer created successfully')
            return redirect('customers')
        else:
            # Add a new customer in complete mode (with every field filled)
            form = CustomerForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return render(request, 'ABC/new_customer.html', {'form': form})

            form.save()
            messages.success(request, 'Customer created successfully')
            return redirect('new_customer')


@login_required
def delete_customer(request, customer_id):
    customer = Customer.objects.get(id=customer_id)
    customer.delete()
    return redirect('customers')


@login_required
def modify_customer(request):
    if request.method == 'POST':
        customer_id = request.POST['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        # Modify a Customer
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_customer.html', {'form': form, 'customer_id': customer_id})

        form.save()
        return redirect('customers')


@login_required
def report_customers(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="customers.pdf"'

    buffer = BytesIO()

    documento = SimpleDocTemplate(buffer, pagesize=A4, rigthMargin=40, leftMargin=40, topMargin=60, bootomMargin=18)
    customers = []
    styles = getSampleStyleSheet()
    header = Paragraph("Customer report", styles['Heading1'])
    customers.append(header)

    table_header = ('Nombre', 'Empresa', 'Dirección')
    datos = [(customer.name, customer.company_name, customer.address) for customer in Customer.objects.all()]
    tabla = Table([table_header] + datos)
    tabla.setStyle(TableStyle([('GRID', (0, 0), (-1, -1), 1, colors.black),]))

    customers.append(tabla)
    documento.build(customers)
    response.write(buffer.getvalue())
    buffer.close()
    return response


@login_required
def customers(request):
    customers = Customer.objects.order_by('name')
    context = {'customers': customers}
    return render(request, 'ABC/customers.html', context)


@login_required
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


@login_required
def customer_info(request):
    customer_id = request.GET.get('customer_id')
    customer = Customer.objects.get(pk=customer_id)
    customer_json = {}
    customer_json['name'] = customer.name
    customer_json['surname'] = customer.surname
    customer_json['company_name'] = customer.company_name
    customer_json['location'] = customer.city + ", " + customer.province
    customer_json['email'] = customer.email
    customer_json['web'] = customer.web
    customer_json['phone'] = customer.phone

    data = json.dumps(customer_json)
    return HttpResponse(data, 'application/json')