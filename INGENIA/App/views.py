from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event, Student, Registration
from .forms import EventForm, RegistrationForm
import csv
import uuid, secrets, string
from django.contrib.auth.decorators import login_required, user_passes_test




def home(request):
    events = Event.objects.all()
    return render(request, 'pages/home.html', {'events': events})

@login_required
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
    registrations_count = Registration.objects.filter(event=event).count()

    if registrations_count >= event.max_participants:
            return render(request, 'pages/register_full.html', {'event': event})

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            registration = Registration.objects.create(event=event, student=student)
            passcode = registration.passcode
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form, 'event': event, 'passcode': passcode})



def event_list(request):
    events = Event.objects.all()
    return render(request, 'pages/event_list.html', {'events': events})

@login_required
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

@login_required
def check_in(request):
    events = Event.objects.all()
    message = ""
    selected_event = None

    if request.method == 'POST':
        event_id = request.POST.get('event')
        passcode = request.POST.get('passcode')
        selected_event = get_object_or_404(Event, id=event_id)

        try:
            registration = Registration.objects.get(event=selected_event, passcode=passcode)
            if registration.attended:
                message = f"Passcode {passcode} has already been used for {registration.student.name}"
            else:
                registration.attended = True
                registration.save()
                message = f"Check-in successful for {registration.student.name}"
        except Registration.DoesNotExist:
            message = "Invalid passcode for the selected event"

    return render(request, 'pages/check_in.html', {'events': events, 'message': message, 'selected_event': selected_event})

def generate_passcode():
    alphabet = string.ascii_letters + string.digits
    while True:
        passcode = ''.join(secrets.choice(alphabet) for _ in range(6))
        if not Registration.objects.filter(passcode=passcode).exists():
            return passcode


