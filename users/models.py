from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default_profile.png', upload_to='profile_pics')

	def __str__(self):
		return f'{self.user.username} Profile'

class Team(models.Model):
    name = models.CharField(max_length=128)
    pin = models.IntegerField(unique=True)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
    	return reverse('home')

class Membership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " + " + self.team.name