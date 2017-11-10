from django.http import HttpResponseRedirect
from django.urls import reverse
from ABC.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from arkaABC.settings import ITEMS_PER_PAGE
from .forms import ItemQuickForm, ItemForm
from django.shortcuts import render


def index(request):
    return render(request, 'ABC/index.html')


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


def item(request, item_id):
    the_item = Item.objects.get(id=item_id)
    context = {'the_item': the_item}
    return render(request, 'ABC/item.html', context)


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


def remove_item(request, item_id):
    an_item = Item.objects.get(id=item_id)
    an_item.delete()
    return HttpResponseRedirect(reverse('items'))


def new_item(request):
    return render(request, 'ABC/new_item.html')


def customers(request):
    return render(request, 'ABC/customers.html')


def providers(request):
    return render(request, 'ABC/providers.html')


def orders(request):
    return render(request, 'ABC/orders.html')


def invoices(request):
    return render(request, 'ABC/invoices.html')


def events(request):
    return render(request, 'ABC/events.html')


def tasks(request):
    return render(request, 'ABC/tasks.html')


def signin(request):
    return render(request, 'ABC/signin.html')
