from django.shortcuts import render
from .models import Ticket, Comment, History, Attachment 
from projects.models import Project
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse

def TicketInfo(request, pk=None):
	if pk:
		ticket = Ticket.objects.get(pk=pk)
	comments = ticket.comment_set.all().order_by('-date_created')
	history_list = ticket.history_set.all().order_by('-date_changed')
	attachments = ticket.attachment_set.all().order_by('-date_created')
	return render(request, 'tickets/ticket_info.html', {'comments': comments, 'ticket':ticket, 'history_list': history_list, 'attachments': attachments})

def my_tickets(request):
	tickets = Ticket.objects.filter(submitter=request.user).order_by('-date_updated')
	return render(request, 'tickets/my_tickets.html', {'tickets':tickets})

class TicketCreateView(LoginRequiredMixin, CreateView):
	model = Ticket
	fields = ['title', 'description', 'priority', 'status', 'ticket_type']

	def get_success_url(self):
		return reverse('project-info', kwargs={'pk': self.kwargs['pk']})

	def form_valid(self, form):
		pk = self.kwargs['pk']
		project = Project.objects.get(pk=pk)
		form.instance.project = project
		form.instance.submitter = self.request.user
		History.objects.create(user=self.request.user, action="Created Ticket", old_value=' ', new_value=form.instance.title)
		return super().form_valid(form)

class TicketUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Ticket
	fields = ['title', 'description', 'priority', 'status', 'ticket_type']

	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})

	def form_valid(self, form):
		form.instance.submitter = self.request.user
		old_ticket = Ticket.objects.get(pk=self.kwargs['pk']).__dict__
		for field, value in old_ticket.items():
			if field in ['title', 'description', 'priority', 'status', 'ticket_type']:
				newval = getattr(form.instance, field)
				if value == newval:
					continue
				else:
					History.objects.create(user=self.request.user, action=f"Updated {field} field", old_value=value, new_value=newval, ticket=self.get_object())
		return super().form_valid(form)

	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter:
			return True
		return False

class TicketDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Ticket
	
	def get_success_url(self):
		project = self.get_object().project
		return reverse('project-info', kwargs={'pk': project.id})
	
	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter:
			return True
		return False

class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	fields = ['message']
	
	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		form.instance.author = self.request.user
		History.objects.create(user=self.request.user, action=f"Created comment", old_value="", new_value=form.instance.message, ticket=form.instance.ticket)
		return super().form_valid(form)

class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Comment
	fields = ['message']

	def get_success_url(self):
		comment = self.get_object()
		ticket = comment.ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def form_valid(self, form):
		form.instance.submitter = self.request.user
		old_comment = Comment.objects.get(pk=self.kwargs['pk']).__dict__
		History.objects.create(user=self.request.user, action=f"Updated Comment", old_value=old_comment['message'], new_value=form.instance.message, ticket=self.get_object().ticket)
		return super().form_valid(form)

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False

class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Comment

	def get_success_url(self):
		ticket = self.get_object().ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def delete(self, request, *args, **kwargs):
		comment = self.get_object()
		History.objects.create(user=self.request.user, action=f"Deleted comment '{comment.message}'", old_value=comment.message, new_value='', ticket=comment.ticket)
		return super(CommentDeleteView, self).delete(request, *args, **kwargs)
	
	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author:
			return True
		return False

class AttachmentCreateView(LoginRequiredMixin, CreateView):
	model = Attachment
	fields = ['title', 'description', 'file']
	
	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		form.instance.poster = self.request.user
		return super().form_valid(form)

class AttachmentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Attachment
	fields = ['title', 'description', 'file']

	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.get_object().ticket.id})

	def form_valid(self, form):
		form.instance.poster = self.request.user
		old_attachment = Attachment.objects.get(pk=self.kwargs['pk']).__dict__
		for field, value in old_attachment.items():
			if field in ['title', 'description', 'file']:
				newval = getattr(form.instance, field)
				if value == newval:
					continue
				else:
					History.objects.create(user=self.request.user, action=f"Updated {field} field on attachment", old_value=value, new_value=newval, ticket=self.get_object().ticket)
		return super().form_valid(form)

	def test_func(self):
		attachment = self.get_object()
		if self.request.user == attachment.poster:
			return True
		return False


class AttachmentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Attachment

	def get_success_url(self):
		ticket = self.get_object().ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def delete(self, request, *args, **kwargs):
		attachment = self.get_object()
		History.objects.create(user=self.request.user, action=f"Deleted attachment '{attachment.title}'", old_value=attachment.title, new_value='', ticket=attachment.ticket)
		return super(AttachmentDeleteView, self).delete(request, *args, **kwargs)
	
	def test_func(self):
		attachment = self.get_object()
		if self.request.user == attachment.poster:
			return True
		return False





