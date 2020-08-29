from django import forms
from django.contrib.auth.models import User
from tickets.models import Ticket

class TicketCreateForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'priority', 'status', 'ticket_type']
