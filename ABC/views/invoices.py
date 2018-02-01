from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ABC.forms import InvoiceForm
from ABC.models import Invoice


@login_required
def new_invoice(request):
    form = InvoiceForm()
    context = {'form': form}
    return render(request, 'ABC/new_invoice.html', context)


@login_required
def invoices(request):
    invoices = Invoice.objects.all()
    context = {'invoices': invoices}
    return render(request, 'ABC/invoices.html', context)


@login_required
def add_invoice(request):
    pass


@login_required
def delete_invoice(request, invoice_id):
    invoice = Invoice.objects.get(pk=invoice_id)
    invoice.delete()
    return redirect('invoices')
