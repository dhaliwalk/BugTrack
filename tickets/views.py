from django.shortcuts import render
from .models import Ticket, Comment, History, Attachment, TicketDev
from projects.models import Project, ProjectHistory
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from .forms import TicketUpdateForm, TicketDevCreateForm, CommentCreateForm, AttachmentCreateForm
from django.forms.models import model_to_dict
from django import forms
from django.db.models import Q
from django.db.models import Case, Value, When, IntegerField

def TicketInfo(request, pk=None):
	if pk:
		ticket = Ticket.objects.get(pk=pk)
	comments = ticket.comment_set.all().order_by('-date_created')
	history_list = ticket.history_set.all().order_by('-date_changed')
	attachments = ticket.attachment_set.all().order_by('-date_created')
	developers = TicketDev.objects.filter(ticket=ticket).order_by('-date_added')
	old_ticket = model_to_dict(ticket).items()
	# paginator = Paginator(comments, 5)
	# page_number = request.GET.get('page')
	# page_obj_comments = paginator.get_page(page_number)

	# paginator = Paginator(history_list, 5)
	# page_number = request.GET.get('page')
	# page_obj_history = paginator.get_page(page_number)

	# paginator = Paginator(developers, 5)
	# page_number = request.GET.get('page')
	# page_obj_devs = paginator.get_page(page_number)

	# paginator = Paginator(attachments, 5)
	# page_number = request.GET.get('page')
	# page_obj_attachments = paginator.get_page(page_number)
	if request.method == 'POST' and 'ticket_edit' in request.POST:
		form = TicketUpdateForm(request.POST, instance=ticket)
		comment_form = CommentCreateForm()
		file_form = AttachmentCreateForm()
		u_form = TicketDevCreateForm()
		current_ticketdevs_ids = ticket.developers.all().values_list('id',flat=True)
		u_form.fields['user'].queryset = (ticket.project.members).exclude(id__in=current_ticketdevs_ids)
		if form.is_valid():
			for field, value in old_ticket:
				if field in ['title', 'description', 'priority', 'status', 'ticket_type']:
					newval = getattr(form.instance, field)
					if value == newval:
						continue
					else:
						History.objects.create(user=request.user, action=f"Updated {field} field", old_value=value, new_value=newval, ticket=ticket, icon_type='update')
			form.save()
			return HttpResponseRedirect(reverse('ticket-info', kwargs={'pk': ticket.id}))
	
	elif request.method == 'POST' and 'user_add' in request.POST:
		form = TicketUpdateForm(instance=ticket)
		comment_form = CommentCreateForm()
		file_form = AttachmentCreateForm()
		u_form = TicketDevCreateForm(request.POST)
		current_ticketdevs_ids = ticket.developers.all().values_list('id',flat=True)
		u_form.fields['user'].queryset = (ticket.project.members).exclude(id__in=current_ticketdevs_ids)
		if u_form.is_valid():
			u_form.instance.ticket = ticket
			History.objects.create(user=request.user, action=f"Added User '{u_form.instance.user.username}'", old_value="", new_value="", ticket=ticket, icon_type='person_add')
			ProjectHistory.objects.create(user=request.user, action=f"Added User '{u_form.instance.user.username}' to Ticket '{ticket.title}' ", old_value="", new_value="", project=ticket.project, icon_type='person_add')
			u_form.save()
			return HttpResponseRedirect(reverse('ticket-info', kwargs={'pk': ticket.id}))
	
	elif request.method == 'POST' and 'comment_add' in request.POST:
		form = TicketUpdateForm(instance=ticket)
		comment_form = CommentCreateForm(request.POST)
		file_form = AttachmentCreateForm()
		u_form = TicketDevCreateForm()
		current_ticketdevs_ids = ticket.developers.all().values_list('id',flat=True)
		u_form.fields['user'].queryset = (ticket.project.members).exclude(id__in=current_ticketdevs_ids)
		if comment_form.is_valid():
			comment_form.instance.ticket = ticket
			comment_form.instance.author = request.user
			History.objects.create(user=request.user, action=f"Created comment", old_value="", new_value=comment_form.instance.message, ticket=ticket, icon_type='add_comment')
			comment_form.save()
			return HttpResponseRedirect(reverse('ticket-info', kwargs={'pk': ticket.id}))
	
	elif request.method == 'POST' and 'file_add' in request.POST:
		form = TicketUpdateForm(instance=ticket)
		comment_form = CommentCreateForm()
		file_form = AttachmentCreateForm(request.POST, request.FILES)
		u_form = TicketDevCreateForm()
		current_ticketdevs_ids = ticket.developers.all().values_list('id',flat=True)
		u_form.fields['user'].queryset = (ticket.project.members).exclude(id__in=current_ticketdevs_ids)
		if file_form.is_valid():
			file_form.instance.ticket = ticket
			file_form.instance.poster = request.user
			History.objects.create(user=request.user, action=f"Added Attachment", old_value="", new_value=file_form.instance.title, ticket=ticket, icon_type='library_add')
			file_form.save()
			return HttpResponseRedirect(reverse('ticket-info', kwargs={'pk': ticket.id}))
	
	else:
		form = TicketUpdateForm(instance=ticket)
		comment_form = CommentCreateForm()
		file_form = AttachmentCreateForm()
		u_form = TicketDevCreateForm()
		current_ticketdevs_ids = ticket.developers.all().values_list('id',flat=True)
		u_form.fields['user'].queryset = (ticket.project.members).exclude(id__in=current_ticketdevs_ids)

	if request.user.membership.team.project_set.filter(pk=ticket.project.id).exists():
		return render(request, 'tickets/ticket_info.html', {'file_form': file_form, 'comment_form': comment_form, 'u_form':u_form, 'form':form, 'comments': comments, 'ticket':ticket, 'history_list': history_list, 'attachments': attachments, 'developers': developers})
	else:
		return HttpResponse('<h1>Not authorized to view this page</h1>')


def my_tickets(request):
	tickets = Ticket.objects.filter(Q(submitter=request.user) | Q(developers=request.user)).order_by('-date_updated')
	tickets = tickets.annotate(custom_order=Case(When(priority='High', then=Value(0)), When(priority='Medium', then=Value(1)), When(priority='Low', then=Value(2)), When(priority='None', then=Value(3)), output_field=IntegerField(),)).order_by('custom_order')
	query = request.GET.get('query')
	if query != None:
		tickets = tickets.filter(title__contains=query)
	if query == '':
		tickets = Ticket.objects.filter(Q(submitter=request.user) | Q(developers=request.user)).order_by('-date_updated')
		tickets = tickets.annotate(custom_order=Case(When(priority='High', then=Value(0)), When(priority='Medium', then=Value(1)), When(priority='Low', then=Value(2)), When(priority='None', then=Value(3)), output_field=IntegerField(),)).order_by('custom_order')

	paginator = Paginator(tickets, 12)
	page_number = request.GET.get('page')
	tickets = paginator.get_page(page_number)

	return render(request, 'tickets/my_tickets.html', {'tickets':tickets, 'query': query})

class TicketCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
	model = Ticket
	fields = ['title', 'description', 'priority', 'status', 'ticket_type']

	def get_success_url(self):
		return reverse('project-info', kwargs={'pk': self.kwargs['pk']})

	def form_valid(self, form):
		project = Project.objects.get(pk=self.kwargs['pk'])
		form.instance.project = project
		form.instance.submitter = self.request.user
		History.objects.create(user=self.request.user, action="Created Ticket", old_value=' ', new_value=form.instance.title, icon_type='library_add')
		ProjectHistory.objects.create(user=self.request.user, action="Created Ticket", old_value=' ', new_value=form.instance.title, project=project, icon_type='library_add')
		return super().form_valid(form)

	def test_func(self):
		project = Project.objects.get(pk=self.kwargs['pk'])
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists():
			return True
		return False


class TicketUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Ticket
	form_class = TicketUpdateForm

	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})

	def form_valid(self, form):
		old_ticket = Ticket.objects.get(pk=self.kwargs['pk']).__dict__
		for field, value in old_ticket.items():
			if field in ['title', 'description', 'priority', 'status', 'ticket_type']:
				newval = getattr(form.instance, field)
				if value == newval:
					continue
				else:
					History.objects.create(user=self.request.user, action=f"Updated {field} field", old_value=value, new_value=newval, ticket=self.get_object(), icon_type='update')
		return super().form_valid(form)

	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter or (self.request.user.membership.team.project_set.filter(pk=ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class TicketDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Ticket
	
	def get_success_url(self):
		project = self.get_object().project
		return reverse('project-info', kwargs={'pk': project.id})
	
	def delete(self, request, *args, **kwargs):
		ticket = self.get_object()
		ProjectHistory.objects.create(user=self.request.user, action=f"Deleted Ticket '{ticket.title}'", old_value='', new_value='', project=ticket.project, icon_type='delete')
		return super(TicketDeleteView, self).delete(request, *args, **kwargs)

	def test_func(self):
		ticket = self.get_object()
		if self.request.user == ticket.submitter or (self.request.user.membership.team.project_set.filter(pk=ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class CommentCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
	model = Comment
	fields = ['message']
	
	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		form.instance.author = self.request.user
		History.objects.create(user=self.request.user, action=f"Created comment", old_value="", new_value=form.instance.message, ticket=form.instance.ticket, icon_type='add_comment')
		return super().form_valid(form)

	def test_func(self):
		ticket = Ticket.objects.get(pk= self.kwargs['pk'])
		if self.request.user.ticket_set.filter(pk=ticket.id).exists() or (self.request.user.membership.team.project_set.filter(pk=ticket.team.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class CommentUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Comment
	fields = ['subject', 'message']

	def get_success_url(self):
		comment = self.get_object()
		ticket = comment.ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def form_valid(self, form):
		form.instance.submitter = self.request.user
		old_comment = Comment.objects.get(pk=self.kwargs['pk']).__dict__
		History.objects.create(user=self.request.user, action=f"Updated Comment", old_value=old_comment['message'], new_value=form.instance.message, ticket=self.get_object().ticket, icon_type='comment')
		return super().form_valid(form)

	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author or (self.request.user.membership.team.project_set.filter(pk=comment.ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class CommentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Comment

	def get_success_url(self):
		ticket = self.get_object().ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def delete(self, request, *args, **kwargs):
		comment = self.get_object()
		History.objects.create(user=self.request.user, action=f"Deleted comment '{comment.message}'", old_value=comment.message, new_value='', ticket=comment.ticket, icon_type='delete')
		return super(CommentDeleteView, self).delete(request, *args, **kwargs)
	
	def test_func(self):
		comment = self.get_object()
		if self.request.user == comment.author or (self.request.user.membership.team.project_set.filter(pk=comment.ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class AttachmentCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
	model = Attachment
	fields = ['title', 'description', 'file']
	
	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		form.instance.poster = self.request.user
		History.objects.create(user=self.request.user, action=f"Added Attachment", old_value="", new_value=form.instance.title, ticket=form.instance.ticket, icon_type='library_add')
		return super().form_valid(form)

	def test_func(self):
		ticket = Ticket.objects.get(pk= self.kwargs['pk'])
		if self.request.user.ticket_set.filter(pk=ticket.id).exists() or (self.request.user.membership.team.project_set.filter(pk=ticket.team.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

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
					History.objects.create(user=self.request.user, action=f"Updated {field} field on attachment", old_value=value, new_value=newval, ticket=self.get_object().ticket, icon_type='update')
		return super().form_valid(form)

	def test_func(self):
		attachment = self.get_object()
		if self.request.user == attachment.poster or (self.request.user.membership.team.project_set.filter(pk=attachment.ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False


class AttachmentDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Attachment

	def get_success_url(self):
		ticket = self.get_object().ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def delete(self, request, *args, **kwargs):
		attachment = self.get_object()
		History.objects.create(user=self.request.user, action=f"Deleted attachment '{attachment.title}'", old_value=attachment.title, new_value='', ticket=attachment.ticket, icon_type='delete')
		return super(AttachmentDeleteView, self).delete(request, *args, **kwargs)
	
	def test_func(self):
		attachment = self.get_object()
		if self.request.user == attachment.poster or (self.request.user.membership.team.project_set.filter(pk=attachment.ticket.project.id).exists() and self.request.user.membership.role == 'Admin'):
			return True
		return False

class TicketDevCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
	model = TicketDev
	fields = ['user']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		current_ticketdevs_ids = Ticket.objects.get(pk=self.kwargs['pk']).developers.all().values_list('id',flat=True)
		form.fields['user'].queryset = (Project.objects.get(pk=Ticket.objects.get(pk=self.kwargs['pk']).project.id).members).exclude(id__in=current_ticketdevs_ids)
		return form

	def get_success_url(self):
		return reverse('ticket-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		pk = self.kwargs['pk']
		form.instance.ticket = Ticket.objects.get(pk=pk)
		History.objects.create(user=self.request.user, action=f"Added User", old_value="", new_value=form.instance.user.username, ticket=form.instance.ticket, icon_type='person_add')
		return super().form_valid(form)

	def test_func(self):
		ticket = Ticket.objects.get(pk=self.kwargs['pk'])
		if self.request.user.ticket_set.filter(pk=ticket.id).exists() and self.request.user.membership.role == 'Admin':
			return True
		return False

class TicketDevDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = TicketDev
	def get_success_url(self):
		ticket = self.get_object().ticket
		return reverse('ticket-info', kwargs={'pk': ticket.id})

	def delete(self, request, *args, **kwargs):
		ticketdev = self.get_object()
		History.objects.create(user=self.request.user, action=f"Removed developer '{ticketdev.user.username}'", old_value='', new_value='', ticket=ticketdev.ticket, icon_type='person_remove')
		ProjectHistory.objects.create(user=self.request.user, action=f"Removed developer '{ticketdev.user.username}' from ticket '{ticketdev.ticket}'", old_value='', new_value='', project=ticketdev.ticket.project, icon_type='person_remove')
		return super(TicketDevDeleteView, self).delete(request, *args, **kwargs)
	
	def test_func(self):
		if self.request.user.ticket_set.filter(pk=self.get_object().ticket.id).exists() and self.request.user.membership.role == 'Admin':
			return True
		return False



