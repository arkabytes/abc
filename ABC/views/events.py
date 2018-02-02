from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from ABC.forms import EventForm
from ABC.models import Event


@login_required
def new_event(request, event_id=None):
    if event_id:
        event = Event.objects.get(pk=event_id)
        form = EventForm(instance=event)
    else:
        form = EventForm()

    context = {'form': form, 'event_id': event_id}
    return render(request, 'ABC/new_event.html', context)


@login_required
def events(request):
    events = Event.objects.all()
    context = {'events': events}
    return render(request, 'ABC/events.html', context)


@login_required
def add_event(request):
    if request.method == 'POST':
        # Add a new event in complete mode (with every field filled)
        form = EventForm(request.POST, request.FILES)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_event.html', {'form': form})

        form.save()
        messages.success(request, 'Event created successfully')
        return redirect('new_event')


@login_required
def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    event.delete()
    return redirect('events')


@login_required
def modify_event(request):
    if request.method == 'POST':
        event_id = request.POST['event_id']
        event = Event.objects.get(pk=event_id)
        # Modifiy a Event
        form = EventForm(request.POST, request.FILES, instance=event)
        if not form.is_valid():
            messages.error(request, 'Some errors has occurred')
            return render(request, 'ABC/new_event.html', {'form': form, 'event_id': event_id})

        form.save()
        return redirect('events')
