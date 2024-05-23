from django.db import models
import uuid
import secrets
import string


class Event(models.Model):
    EVENT_TYPES = [
        ('course', 'Course'),
        ('conference', 'Conference'),
        ('workshop', 'Workshop'),
    ]
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateField()
    max_participants = models.PositiveIntegerField()
    reviews_enabled = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name
    
def generate_passcode():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(6))

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    passcode = models.CharField(max_length=6, default=generate_passcode, unique=True)
    attended = models.BooleanField(default=False)
    review = models.TextField(blank=True, null=True)
    rating = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.name} - {self.event.name}"