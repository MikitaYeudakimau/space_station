from django.db import models
from django.contrib.auth.models import User


class SpaceStation(models.Model):
    """
    SpaceStation model
    """
    RUNNING = "running"
    BROKEN = "broken"
    CONDITION_CHOICES = [
        (RUNNING, "running"),
        (BROKEN, "broken")
    ]
    name = models.CharField(max_length=50, unique=True)
    condition = models.CharField(max_length=8, choices=CONDITION_CHOICES, default=RUNNING)
    position_x = models.IntegerField(default=100)
    position_y = models.IntegerField(default=100)
    position_z = models.IntegerField(default=100)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_broken = models.DateTimeField(blank=True, null=True)


class Pointing(models.Model):
    """
    Pointing model for changing space_station positions
    """
    X = "x"
    Y = "y"
    Z = "z"
    AXIS_CHOICES = [
        (X, "Axis X"),
        (Y, "Axis Y"),
        (Z, "Axis Z"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pointing_user")
    axis = models.CharField(max_length=2, choices=AXIS_CHOICES)
    distance = models.IntegerField()
