from django.db import models
import uuid

# Create your models here.


class Event(models.Model):
    EVENT_TYPES = [
        ('course', 'Course')
    ]
    name = models.CharField(max_length=100)
    event_type = models.CharField(max_length=10, choices=EVENT_TYPES)
    description = models.TextField()
    date = models.DateField()

    def __str__(self):
        return self.name
    

class Student(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    passcode = models.UUIDField(default=uuid.uuid4, editable=False)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.name} - {self.event.name}"