from django.db import models
from django.contrib.auth.models import User
from users.models import Team
from django.urls import reverse

class Project(models.Model):
	name = models.CharField(max_length=128)
	description = models.CharField(max_length=500)
	members = models.ManyToManyField(User, through='ProjectMember')
	team = models.ForeignKey(Team, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name
	
	def get_absolute_url(self):
		return reverse('home')

class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username + " + " + self.project.name

class ProjectHistory(models.Model):
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	action = models.CharField(max_length=128)
	old_value = models.CharField(max_length=128)
	new_value = models.CharField(max_length=128)
	date_changed = models.DateTimeField(auto_now_add=True)
	icon_type = models.CharField(max_length=200)

	def __str__(self):
		return self.user.username + " " + self.action 