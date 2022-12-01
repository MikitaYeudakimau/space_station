from django.db import models
from django.contrib.auth.models import User

class SpaceStation(models.Model):
    RUNNING = "running"
    BROKEN = "broken"
    CONDITION_CHOICES = [
        (RUNNING,"running"),
        (BROKEN,"broken")
    ]
    name = models.CharField(max_length=50, unique=True)
    condition = models.CharField(default=RUNNING)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_broken = models.DateTimeField(blank=True)

class Pointing(models.Model):
    X= "x"
    Y= "y"
    Z= "z"
    AXIS_CHOICES = [
        (X,"Axis X"),
        (Y, "Axis Y"),
        (Z, "Axis Z"),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="pointing_user")
    axis = models.CharField(choices=AXIS_CHOICES)
    distance = models.IntegerField