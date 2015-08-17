from django.db import models

from django.contrib.auth.models import User

__all__ = [
    'Contributor',
    'Session',
    'StaffRegistration',
    'StudentRegistration',
]

class Contributor(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    name = models.CharField(max_length=128)
    irc_nick = models.CharField(max_length=50)

class Session(models.Model):
    name = models.CharField(max_length=128)
    maximum_students = models.IntegerField()
    start_date = models.DateTimeField()
    
class StaffRegistration(models.Model):
    contributor = models.ForeignKey(Contributor)
    session = models.ForeignKey(Session)
    mentor_capacity = models.IntegerField(default=0)
    assistant = models.BooleanField(default=True)
    instructor = models.BooleanField(default=True)

class StudentRegistration(models.Model):
    status_codes = (
        ('active', 'Active'),
        ('complete', 'Complete'),
        ('new', 'New'),
        ('waitlist', 'Wait list'),
        ('withdrawn', 'withdrawn'),
    )

    contributor = models.ForeignKey(Contributor)
    mentor = models.ForeignKey(Contributor, related_name='+')
    session = models.ForeignKey(Session)

    registration_date = models.DateTimeField()
    status = models.CharField(choices=status_codes, max_length=128)

