from django.db import models
from django.contrib.auth.models import User
from projects.models import Project

class Ticket(models.Model):
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=500)
	submitter = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
	priority = models.CharField(max_length=128)
	status = models.CharField(max_length=128)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	ticket_type = models.CharField(max_length=128)
