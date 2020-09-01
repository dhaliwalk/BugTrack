from django.db import models
from django.contrib.auth.models import User
from projects.models import Project
from django.urls import reverse

class Ticket(models.Model):
	status_choices = [
		("OPEN", "Open"),
		("IN_PROGRESS", "In Progress"),
		("RESOLVED", "Resolved"),
		("CLOSED", "Closed"),
		("WAITING_ON_MORE_INFO", "Waiting on More Info"),
	]
	priority_choices = [
		("HIGH", "High"),
		("MEDIUM", "Medium"),
		("LOW", "Low"),
		("NONE", "None"),
	]
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=500)
	submitter = models.ForeignKey(User, on_delete=models.CASCADE)
	project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
	priority = models.CharField(max_length=128, choices=priority_choices, default="None")
	status = models.CharField(max_length=128, choices=status_choices, default="OPEN")
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	ticket_type = models.CharField(max_length=128)
	developers = models.ManyToManyField(User, through='TicketDev', related_name='ticket_developers')

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home')

class Comment(models.Model):
	subject = models.CharField(max_length=128)
	message = models.CharField(max_length=500)
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	def __str__(self):
		return self.message

	def get_absolute_url(self):
		return reverse('home')

class Attachment(models.Model):
	file = models.FileField(upload_to='ticket_attachments_bugtrack')
	title = models.CharField(max_length=128)
	description = models.CharField(max_length=500)
	poster = models.ForeignKey(User, on_delete=models.CASCADE)
	date_created = models.DateTimeField(auto_now_add=True)
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('home')

class History(models.Model):
	ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	action = models.CharField(max_length=128)
	old_value = models.CharField(max_length=128)
	new_value = models.CharField(max_length=128)
	date_changed = models.DateTimeField(auto_now_add=True)
	icon_type = models.CharField(max_length=200)

	def __str__(self):
		return self.user.username + " " + self.action 

class TicketDev(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username + " + " + self.ticket.title




