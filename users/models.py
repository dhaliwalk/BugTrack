from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default_profile.png', upload_to='profile_pics_bugtrack')

	def __str__(self):
		return f'{self.user.username} Profile'

class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    pin = models.IntegerField()
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
    	return reverse('home')

class Membership(models.Model):
    role_choices = [
        ("Admin", "Admin"),
        ("Developer", "Developer"),
        ("Project Manager", "Project Manager"),
        ("Client", "Client"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=128, choices=role_choices, default="None")
    def __str__(self):
        return self.user.username + " + " + self.team.name + " Role:" + self.role