from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.urls import reverse

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

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home')

class Comment(models.Model):
	message = models.CharField(max_length=500)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	def __str__(self):
		return self.message

	def get_absolute_url(self):
		return reverse('home')

class History(models.Model):
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	action = models.CharField(max_length=128)
	old_value = models.CharField(max_length=128)
	new_value = models.CharField(max_length=128)
	date_changed = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.username + " " + self.action + " on ticket " + self.ticket.title