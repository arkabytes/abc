from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('ABC/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def items(request):
    template = loader.get_template('ABC/items.html')
    context = {}
    return HttpResponse(template.render(context, request))
