from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, ProjectMember, ProjectHistory
from users.models import Team
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse
from .forms import TicketCreateForm, ProjectUpdateForm, ProjectMemberCreateForm
from django.http import HttpResponse, HttpResponseRedirect
from tickets.models import History
from django.forms.models import model_to_dict
from django.db.models import Q, Case, Value, When, IntegerField
from datetime import datetime

# def list(request):
# 	user = request.user
# 	role = user.membership.role
# 	team = user.membership.team
# 	if role == 'Admin':
# 		projects = team.project_set.all().order_by('name')
# 	else:
# 		projects = team.project_set.filter(members=user).order_by('name')

# 	paginator = Paginator(projects, 10)
# 	page_number = request.GET.get('page')
# 	page_obj = paginator.get_page(page_number)
	
# 	return render(request, 'projects/project_list.html', {'page_obj': page_obj, 'role': role})

# def ProjectJoin(request, pk=None):
# 	if pk:
# 		project = Project.objects.get(pk=pk)
# 	if request.method == 'POST':
# 		instance = ProjectMember(user=request.user, project=Project.objects.get(pk=pk))
# 		instance.save()
# 		messages.success(request, 'You have joined the project {{ project.name }}')
# 		return redirect('home')			
# 	return render(request, 'projects/project_join.html', {'project': project})

def ProjectInfo(request, pk=None):
	if pk:
		project = Project.objects.get(pk=pk)
	date = datetime.today().date()
	members = ProjectMember.objects.filter(project=project)
	tickets = project.ticket_set.all().order_by('-date_created')
	tickets = tickets.annotate(custom_order=Case(When(priority='High', then=Value(0)), When(priority='Medium', then=Value(1)), When(priority='Low', then=Value(2)), When(priority='None', then=Value(3)), When(status='Closed', then=Value(4)), output_field=IntegerField(),), custom_order2=Case(When(status='Closed', then=Value(1)), When(status='Resolved', then=Value(1)), default=Value(0), output_field=IntegerField(),)).order_by('custom_order2', 'custom_order')
	history_list = project.projecthistory_set.all().order_by('-date_changed')
	old_project = model_to_dict(project).items()
	query = request.GET.get('query')

	if request.method == 'POST' and 'ticket_form' in request.POST:
		form = TicketCreateForm(request.POST)
		u_form = ProjectUpdateForm(instance=project)
		member_form = ProjectMemberCreateForm()
		current_projectdevs_ids = Project.objects.get(pk=project.id).members.all().values_list('id',flat=True)
		member_form.fields['user'].queryset = Team.objects.get(pk=project.team.id).members.exclude(id__in=current_projectdevs_ids)
		if form.is_valid():
			form.instance.submitter = request.user
			form.instance.project = project 
			ProjectHistory.objects.create(user=request.user, action=f"Created Ticket '{form.instance.title}' ", old_value='', new_value='', project=project, icon_type='library_add')
			form.save()
			return HttpResponseRedirect(reverse('project-info', kwargs={'pk': project.id}))

	elif request.method == 'POST' and 'update_form' in request.POST:
		u_form = ProjectUpdateForm(request.POST, instance=project)
		form = TicketCreateForm()
		member_form = ProjectMemberCreateForm()
		current_projectdevs_ids = Project.objects.get(pk=project.id).members.all().values_list('id',flat=True)
		member_form.fields['user'].queryset = Team.objects.get(pk=project.team.id).members.exclude(id__in=current_projectdevs_ids)
		if u_form.is_valid():
			for field, value in old_project:
				if field in ['name', 'description']:
					newval = getattr(u_form.instance, field)
					if value == newval:
						continue
					else:
						ProjectHistory.objects.create(user=request.user, action=f"Updated {field} field", old_value=value, new_value=newval, project=project, icon_type='update')
			u_form.save()
			return HttpResponseRedirect(reverse('project-info', kwargs={'pk': project.id}))

	elif request.method == 'POST' and 'member_submit' in request.POST:
		u_form = ProjectUpdateForm(instance=project)
		form = TicketCreateForm()
		member_form = ProjectMemberCreateForm(request.POST)
		current_projectdevs_ids = Project.objects.get(pk=project.id).members.all().values_list('id',flat=True)
		member_form.fields['user'].queryset = Team.objects.get(pk=project.team.id).members.exclude(id__in=current_projectdevs_ids)
		if member_form.is_valid():
			member_form.instance.project = project
			ProjectHistory.objects.create(user=request.user, action=f"Added User '{member_form.instance.user.username}' ", old_value='', new_value='', project=project, icon_type='person_add')
			member_form.save()
			return HttpResponseRedirect(reverse('project-info', kwargs={'pk': project.id}))

	else:
		form = TicketCreateForm()
		u_form = ProjectUpdateForm(instance=project)
		member_form = ProjectMemberCreateForm()
		current_projectdevs_ids = Project.objects.get(pk=project.id).members.all().values_list('id',flat=True)
		member_form.fields['user'].queryset = Team.objects.get(pk=project.team.id).members.exclude(id__in=current_projectdevs_ids)


	if query != None:
		tickets = tickets.filter(Q(title__icontains=query) | Q(priority__icontains=query) | Q(status__icontains=query) | Q(ticket_type__icontains=query)).distinct()
	if query == '':
		tickets = project.ticket_set.all().order_by('-date_created')
		tickets = tickets.annotate(custom_order=Case(When(priority='High', then=Value(0)), When(priority='Medium', then=Value(1)), When(priority='Low', then=Value(2)), When(priority='None', then=Value(3)), When(status='Closed', then=Value(4)), output_field=IntegerField(),), custom_order2=Case(When(status='Closed', then=Value(1)), When(status='Resolved', then=Value(1)), default=Value(0), output_field=IntegerField(),)).order_by('custom_order2', 'custom_order')
	paginator = Paginator(tickets, 12)
	page_number = request.GET.get('page')
	tickets = paginator.get_page(page_number)

	if request.user.project_set.filter(pk=project.id).exists() or (request.user.membership.team.project_set.filter(pk=project.id).exists() and request.user.membership.role == 'Admin'):
		return render(request, 'projects/project_info.html', 
			{'member_form': member_form,'u_form': u_form, 'form': form, 'project':project,  
			'tickets': tickets,
			'members': members,
			'history_list': history_list,
			'query': query,
			'date': date})
	else:
		return HttpResponse('<h1>Not authorized to view this page</h1>')

# class ProjectCreateView(LoginRequiredMixin, CreateView):
# 	model = Project
# 	fields = ['name', 'description']

# 	def form_valid(self, form):
# 		form.instance.team = self.request.user.team_set.first()
# 		return super().form_valid(form)

class ProjectUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Project
	fields = ['name', 'description']

	def get_success_url(self):
		return reverse('project-info', kwargs={'pk': self.get_object().id})

	def form_valid(self, form):
		old_project = Project.objects.get(pk=self.kwargs['pk']).__dict__
		for field, value in old_project.items():
			if field in ['name', 'description']:
				newval = getattr(form.instance, field)
				if value == newval:
					continue
				else:
					ProjectHistory.objects.create(user=self.request.user, action=f"Updated {field} field", old_value=value, new_value=newval, project=self.get_object(), icon_type='update')
		return super().form_valid(form)

	def test_func(self):
		project = self.get_object()
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and (self.request.user.membership.role == 'Admin' or self.request.user.membership.role == 'Project Manager'):
			return True
		return False

class ProjectDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Project

	def get_success_url(self):
		return reverse('team-list')
	
	def test_func(self):
		project = self.get_object()
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and (self.request.user.membership.role == 'Admin' or self.request.user.membership.role == 'Project Manager'):
			return True
		return False

class ProjectMemberCreateView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
	model = ProjectMember
	fields = ['user']

	def get_form(self, form_class=None):
		form = super().get_form(form_class)
		current_projectdevs_ids = Project.objects.get(pk=self.kwargs['pk']).members.all().values_list('id',flat=True)
		form.fields['user'].queryset = Team.objects.get(pk=Project.objects.get(pk=self.kwargs['pk']).team.id).members.exclude(id__in=current_projectdevs_ids)
		return form

	def get_success_url(self):
		return reverse('project-info', kwargs={'pk': self.kwargs['pk']})
	
	def form_valid(self, form):
		project = Project.objects.get(pk=self.kwargs['pk'])
		form.instance.project = project
		return super().form_valid(form)

	def test_func(self):
		project = Project.objects.get(pk=self.kwargs['pk'])
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and self.request.user.membership.role == 'Admin':
			return True
		return False

class ProjectMemberDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = ProjectMember
	def get_success_url(self):
		project = self.get_object().project
		return reverse('project-info', kwargs={'pk': project.id})

	def delete(self, request, *args, **kwargs):
		project_member = self.get_object()
		ProjectHistory.objects.create(user=self.request.user, action=f"Removed User '{project_member.user.username}", old_value='', new_value='', project=project_member.project, icon_type='person_remove')
		return super(ProjectMemberDeleteView, self).delete(request, *args, **kwargs)

	def test_func(self):
		project = self.get_object().project
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and (self.request.user.membership.role == 'Admin' or self.request.user.membership.role == 'Project Manager'):
			return True
		return False



		