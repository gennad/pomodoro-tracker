from django.db import models

class PomadoroModel(models.Model):
    question = models.CharField(max_length=200)
    start = models.DateTimeField(auto_now=True)
    end = models.DateTimeField()
    notes = models.CharField(max_length=1024)
    task = models.CharField(max_length=500)
    squashed = models.BooleanField(default=False)

class TaskModel(models.Model):
    task = models.CharField(max_length=500)
    pomadoros_nedd = models.IntegerField()
    pomadoros_used = models.ForeignKey(PomadoroModel)

from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40)
    key_expires = models.DateTimeField()
