from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

class Project(models.Model):
    title = models.CharField(max_length=255)
    max_players = models.PositiveIntegerField(default=0)
    has_actor = models.BooleanField(default=False)
    scenario = models.TextField()
    #number_of_riddles = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')

    def get_absolute_url(self):
        return reverse(
            "rooms:project_list",
            kwargs={
                "username": self.user.username,
                #"pk": self.pk
            }
        )

class Riddle(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
