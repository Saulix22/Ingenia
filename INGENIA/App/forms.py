from django import forms
from .models import Event, Student, Registration

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'event_type', 'description', 'date', 'max_participants']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['review', 'rating']

class PasscodeForm(forms.Form):
    name = forms.CharField(max_length=200)
    passcode = forms.CharField(max_length=6)

class ToggleReviewsForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['reviews_enabled']