from django.shortcuts import render
from .models import Ticket, Comment 
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView

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

class TicketUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Ticket
	fields = ['title', 'description', 'priority', 'status', 'ticket_type']

	def form_valid(self, form):
		form.instance.submitter = self.request.user
		return super().form_valid(form)

	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter:
			return True
		return False

class TicketDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Ticket
	success_url = "/"
	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter:
			return True
		return False

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	fields = ['message']

	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		form.instance.author = self.request.user
		return super().form_valid(form)

class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Comment
	fields = ['message']

	def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False

class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Comment
	success_url = "/"
	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False




