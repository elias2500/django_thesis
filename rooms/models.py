from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Room(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')
    title = models.CharField(max_length=256)
    noOfPlayers = models.PositiveSmallIntegerField(blank=True)
    difficulty = models.CharField(max_length=10, blank=True)
    hasActor = models.BooleanField(blank=True)
    theme = models.CharField(max_length=256, blank=True)
    scenario = models.TextField(blank=True)
    #noOfRiddles = models.PositiveSmallIntegerField(blank=True)
    riddles = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse(
            "rooms:single",
            kwargs={
                "username": self.user.username,
                "pk": self.pk
            }
        )

    class Meta:
        unique_together = ['user','title']