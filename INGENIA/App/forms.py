from django import forms
from .models import Event, Student

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'description', 'date']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']
