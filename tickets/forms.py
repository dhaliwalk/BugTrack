from django import forms
from django.contrib.auth.models import User
from .models import Ticket, TicketDev, Comment, Attachment

class TicketUpdateForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'priority', 'status', 'ticket_type']

class TicketDevCreateForm(forms.ModelForm):
	class Meta:
		model = TicketDev
		fields = ['user']

class CommentCreateForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['subject', 'message']

class AttachmentCreateForm(forms.ModelForm):
	class Meta:
		model = Attachment
		fields = ['title', 'description', 'file']