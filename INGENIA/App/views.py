from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Student, Registration
from .forms import EventForm, RegistrationForm
import csv
import uuid, secrets, string


def home(request):
    return render(request, 'pages/home.html')


def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'pages/create_event.html', {'form': form})

def register(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    passcode = None
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            registration = Registration.objects.create(event=event, student=student)
            passcode = registration.passcode
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form, 'event': event, 'passcode': passcode})



def check_in(request, passcode):
    registration = get_object_or_404(Registration, passcode=passcode)
    registration.attended = True
    registration.save()
    return HttpResponse("Check-in successful")

def event_list(request):
    events = Event.objects.all()
    return render(request, 'pages/event_list.html', {'events': events})

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

def check_in(request):
    message = ""
    if request.method == 'POST':
        passcode = request.POST.get('passcode')
        try:
            registration = Registration.objects.get(passcode=passcode)
            registration.attended = True
            registration.save()
            message = f"Check-in successful for {registration.student.name}"
        except Registration.DoesNotExist:
            message = "Invalid passcode"
    return render(request, 'pages/check_in.html', {'message': message})

def generate_passcode():
    alphabet = string.ascii_letters + string.digits
    while True:
        passcode = ''.join(secrets.choice(alphabet) for _ in range(6))
        if not Registration.objects.filter(passcode=passcode).exists():
            return passcode
