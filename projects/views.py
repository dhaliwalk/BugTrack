from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, ProjectMember
from users.models import Team
from django.contrib import messages
from django.views.generic import CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.core.paginator import Paginator
from django.http import HttpResponse

def list(request):
	user = request.user
	role = user.membership.role
	team = user.membership.team
	if role == 'Admin':
		projects = team.project_set.all().order_by('name')
	else:
		projects = team.project_set.filter(members=user).order_by('name')

	paginator = Paginator(projects, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	return render(request, 'projects/project_list.html', {'page_obj': page_obj, 'role': role})

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
	members = ProjectMember.objects.filter(project=project)
	tickets = project.ticket_set.all().order_by('-date_created')

	paginator = Paginator(tickets, 5)
	page_number = request.GET.get('page')
	page_obj_tickets = paginator.get_page(page_number)

	paginator = Paginator(members, 5)
	page_number = request.GET.get('page')
	page_obj_members = paginator.get_page(page_number)

	if request.user.project_set.filter(pk=project.id).exists() or (request.user.membership.team.project_set.filter(pk=project.id).exists() and request.user.membership.role == 'Admin'):
		return render(request, 'projects/project_info.html', 
			{'project':project,  
			'page_obj_tickets': page_obj_tickets,
			'page_obj_members': page_obj_members})
	else:
		return HttpResponse('<h1>Not authorized to view this page</h1>')

class ProjectCreateView(LoginRequiredMixin, CreateView):
	model = Project
	fields = ['name', 'description']

	def form_valid(self, form):
		form.instance.team = self.request.user.team_set.first()
		return super().form_valid(form)

class ProjectUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Project
	fields = ['name', 'description']

	def get_success_url(self):
		return reverse('project-info', kwargs={'pk': self.get_object().id})

	def test_func(self):
		project = self.get_object()
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and self.request.user.membership.role == 'Admin':
			return True
		return False

class ProjectDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Project

	def get_success_url(self):
		return reverse('project-list')
	
	def test_func(self):
		project = self.get_object()
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and self.request.user.membership.role == 'Admin':
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
	
	def test_func(self):
		project = self.get_object().project
		if self.request.user.membership.team.project_set.filter(pk=project.id).exists() and self.request.user.membership.role == 'Admin':
			return True
		return False



		