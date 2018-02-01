import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe

from ABC.forms import ItemForm, ItemQuickForm
from ABC.models import Item
from arkaABC.settings import ITEMS_PER_PAGE


@login_required
def item(request, item_id):
    item = Item.objects.get(id=item_id)
    context = {'the_item': item}
    return render(request, 'ABC/item.html', context)


@login_required
def new_item(request, item_id=None):
    if item_id:
        item = Item.objects.get(pk=item_id)
        form = ItemForm(instance=item)
    else:
        form = ItemForm()

    context = {'form': form, 'item_id': item_id}
    return render(request, 'ABC/new_item.html', context)


@login_required
def add_item(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new item in quick mode
            form = ItemQuickForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return redirect('items')

            form.save()
            messages.success(request, 'Item created successfully')
            return redirect('items')
        else:
            # Add a new item in complete mode (with every field filled)
            form = ItemForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return render(request, 'ABC/new_item.html', {'form': form})

            form.save()
            messages.success(request, 'Item created successfully')
            return redirect('new_item')


@login_required
def delete_item(request, item_id):
    item = Item.objects.get(id=item_id)
    item.delete()
    return redirect('items')


@login_required
def modify_item(request):
    if request.method == 'POST':
        item_id = request.POST['item_id']
        item = Item.objects.get(pk=item_id)
        # Modify a Item
        form = ItemForm(request.POST, request.FILES, instance=item)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_item.html', {'form': form, 'item_id': item_id})

        form.save()
        messages.success(request, 'Item modified successfully')
        return redirect('items')


@login_required
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


@login_required
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

        if item.provider is not None:
            item_json['provider_name'] = item.provider.name
        else:
            item_json['provider_name'] = 'No provider'

        if item.vat_type:
            item_json['vat'] = item.vat_type.rate
        else:
            item_json['vat'] = 0
        results.append(item_json)

    data = json.dumps(results)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


@login_required
def item_info(request):
    item_id = request.GET.get('item_id')
    item = Item.objects.get(pk=item_id)
    item_json = {}
    item_json['name'] = item.name
    item_json['description'] = mark_safe(item.description)
    if item.provider is not None:
        item_json['provider_name'] = item.provider.name
    else:
        item_json['provider_name'] = 'No provider'
    item_json['cost_price'] = item.cost_price
    item_json['retail_price'] = item.retail_price
    if item.thumbnail is not None:
        item_json['thumbnail'] = item.thumbnail.url
    else:
        item_json['thumbnail'] = 'item.png'

    data = json.dumps(item_json)
    return HttpResponse(data, 'application/json')
