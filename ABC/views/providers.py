import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render

from ABC.forms import ProviderForm, ProviderQuickForm
from ABC.models import Provider


@login_required
def new_provider(request, provider_id=None):
    if provider_id:
        provider = Provider.objects.get(pk=provider_id)
        form = ProviderForm(instance=provider)
    else:
        form = ProviderForm()

    context = {'form': form, 'provider_id': provider}
    return render(request, 'ABC/new_provider.html', context)


@login_required
def add_provider(request):
    if request.method == 'POST':
        if request.POST['mode'] == 'quick':
            # Add a new provider in quick mode
            form = ProviderQuickForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors occurred')
                return redirect('providers')

            form.save()
            messages.success(request, 'Provider created successfully')
            return redirect('providers')
        else:
            # Add a new provider in complete mode (with every field filled)
            form = ProviderForm(request.POST, request.FILES)
            if not form.is_valid():
                messages.error(request, 'Some errors has occurred')
                return render(request, 'ABC/new_provider.html', {'form': form})

            form.save()
            messages.success(request, 'Provider created successfully')
            return redirect('new_provider')


@login_required
def delete_provider(request, provider_id):
    provider = Provider.objects.get(id=provider_id)
    provider.delete()
    return redirect('providers')


@login_required
def modify_provider(request):
    if request.method == 'POST':
        provider_id = request.POST['provider_id']
        provider = Provider.objects.get(pk=provider_id)
        # Modifiy a VAT Type
        form = ProviderForm(request.POST, request.FILES, instance=provider)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_provider.html', {'form': form, 'provider_id': provider_id})

        form.save()
        messages.success(request, 'Provider modified successfully')
        return redirect('providers')


@login_required
def providers(request):
    providers = Provider.objects.all()
    context = {'providers': providers}
    return render(request, 'ABC/providers.html', context)


@login_required
def provider_info(request):
    provider_id = request.GET.get('provider_id')
    provider = Provider.objects.get(pk=provider_id)
    provider_json = {}
    provider_json['name'] = provider.name
    provider_json['contact_name'] = provider.contact_name
    provider_json['location'] = provider.city + ", " + provider.province
    provider_json['email'] = provider.email
    provider_json['web'] = provider.web
    provider_json['phone'] = provider.phone

    data = json.dumps(provider_json)
    return HttpResponse(data, 'application/json')