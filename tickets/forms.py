from django import forms
from django.contrib.auth.models import User
from .models import Ticket

class TicketUpdateForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'priority', 'status', 'ticket_type']