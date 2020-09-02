from django import forms
from django.contrib.auth.models import User
from tickets.models import Ticket
from .models import Project, ProjectMember

class TicketCreateForm(forms.ModelForm):
	class Meta:
		model = Ticket
		fields = ['title', 'description', 'priority', 'status', 'ticket_type', 'deadline']
		widgets = {
			'deadline': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a Date', 'type':'date'})
		}
class ProjectUpdateForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'description']

class ProjectMemberCreateForm(forms.ModelForm):
	class Meta:
		model = ProjectMember
		fields = ['user']