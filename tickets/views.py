from django.shortcuts import render
from .models import Ticket 
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView

def TicketInfo(request, pk=None):
	if pk:
		ticket = Ticket.objects.get(pk=pk)
	comments = ticket.comment_set.all()
	return render(request, 'tickets/ticket_info.html', {'comments': comments, 'ticket':ticket})

class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	fields = ['title', 'description', 'priority', 'status', 'ticket_type']

	def form_valid(self, form):
		pk = self.kwargs['pk']
		project = Project.objects.get(pk=pk)
		form.instance.project = project
		form.instance.submitter = self.request.user
		return super().form_valid(form)
