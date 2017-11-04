from django.http import HttpResponseRedirect, HttpResponse
from django.template import loader
from django.urls import reverse
from ABC.models import Item


def index(request):
    template = loader.get_template('ABC/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def items(request):
    all_items = Item.objects.order_by('name')

    template = loader.get_template('ABC/items.html')
    context = {'items': all_items,}
    return HttpResponse(template.render(context, request))


def item(request, item_id):
    template = loader.get_template('ABC/item.html')
    the_item = Item.objects.get(id=item_id)
    context = {'the_item':the_item}
    return HttpResponse(template.render(context, request))


def add_item(request):
    an_item = Item.create(request.GET['name'], request.GET['description'], request.GET['price'])
    an_item.save()
    return HttpResponseRedirect(reverse('items'))


def remove_item(request, item_id):
    an_item = Item.objects.get(id=item_id)
    an_item.delete()
    return HttpResponseRedirect(reverse('items'))


def tasks(request):
    template = loader.get_template('ABC/tasks.html')
    context = {}
    return HttpResponse(template.render(context, request))


def signin(request):
    template = loader.get_template('ABC/signin.html')
    context = {}
    return HttpResponse(template.render(context, request))
