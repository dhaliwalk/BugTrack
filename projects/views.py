from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Project, ProjectMember
from users.models import Team
from django.contrib import messages
from django.views.generic import CreateView


def list(request):
	user = request.user
	team = user.team_set.first()
	projects = team.project_set.filter(members=user)
	role = user.membership_set.first().role
	return render(request, 'projects/project_list.html', {'projects': projects, 'role': role})

def ProjectJoin(request, pk=None):
	if pk:
		project = Project.objects.get(pk=pk)
	if request.method == 'POST':
		instance = ProjectMember(user=request.user, project=Project.objects.get(pk=pk))
		instance.save()
		messages.success(request, 'You have joined the project {{ project.name }}')
		return redirect('home')			
	return render(request, 'projects/project_join.html', {'project': project})

def ProjectInfo(request, pk=None):
	if pk:
		project = Project.objects.get(pk=pk)
	tickets = project.ticket_set.all()
	return render(request, 'projects/project_info.html', {'tickets': tickets, 'project':project})

class ProjectCreateView(LoginRequiredMixin, CreateView):
	model = Project
	fields = ['name', 'description']

	def form_valid(self, form):
		form.instance.team = self.request.user.team_set.first()
		return super().form_valid(form)
