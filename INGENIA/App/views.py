from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Student, Registration
from .forms import EventForm, RegistrationForm
import csv

def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})

def register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            Registration.objects.create(event=event, student=student)
            return redirect('event_list')
    else:
        form = RegistrationForm()
    return render(request, 'events/register.html', {'form': form, 'event': event})

def check_in(request, passcode):
    registration = get_object_or_404(Registration, passcode=passcode)
    registration.attended = True
    registration.save()
    return HttpResponse("Check-in successful")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})

def export_attendees(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    registrations = Registration.objects.filter(event=event, attended=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{event.name}_attendees.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Email'])
    for registration in registrations:
        writer.writerow([registration.student.name, registration.student.email])

    return response