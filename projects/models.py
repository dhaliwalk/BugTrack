from django.db import models
from django.contrib.auth.models import User
from users.models import Team
from django.urls import reverse

class Project(models.Model):
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=500)
	members = models.ManyToManyField(User, through='ProjectMember')
	team = models.ForeignKey(Team, on_delete=models.CASCADE)

	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('home')

class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " + " + self.project.name