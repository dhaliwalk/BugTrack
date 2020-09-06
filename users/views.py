from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TeamJoinForm, TeamCreationForm, ProjectCreateForm, TeamUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Team, Membership
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.core.paginator import Paginator
from .decorators import unauthenticated_user
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db.models import Q

@unauthenticated_user
def RegisterUserJoinTeam(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		form_t = TeamJoinForm(request.POST)
		if form.is_valid() and form_t.is_valid():
			form.save()
			user = User.objects.get(username=form.cleaned_data.get('username'))
			if Team.objects.filter(name=form_t.cleaned_data.get('team_name')).count() == 0:
				messages.warning(request, 'Invalid Team Name')
				return render(request, 'users/register_join.html', {'form': form, 'form_t': form_t})
			else:
				team = Team.objects.get(name=form_t.cleaned_data.get('team_name'))
				if int(form_t.cleaned_data.get('team_pin')) == int(team.pin):
					instance = Membership(user=user, team=team, role='unassigned')
					instance.save()
				else:
					messages.warning(request, 'Invalid Pin')
					return render(request, 'users/register_join.html', {'form': form, 'form_t': form_t})
			messages.success(request, 'You account has been created you can now log in!')
			return redirect('login')
	else:
		form = UserRegisterForm()
		form_t = TeamJoinForm()
	return render(request, 'users/register_join.html', {'form': form, 'form_t': form_t})

@unauthenticated_user
def RegisterUserCreateTeam(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		form_t = TeamCreationForm(request.POST)
		if form.is_valid() and form_t.is_valid():
			form.save()
			form_t.save()
			user = User.objects.get(username=form.cleaned_data.get('username'))
			team = Team.objects.get(name=form_t.cleaned_data.get('name'))
			instance = Membership(user=user, team=team, role='unassigned')
			instance.save()
			messages.success(request, 'You account and team has been created you can now log in!')
			return redirect('login')
		else:
			messages.warning(request, 'Fields are Invalid')
	else:
		form = UserRegisterForm()
		form_t = TeamCreationForm()
	return render(request, 'users/register_create.html', {'form': form, 'form_t': form_t})


@login_required
def profile(request):
	if request.method == 'POST' and 'profile_update' in request.POST:
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		pass_form =PasswordChangeForm(user=request.user)
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'Your account has been updated')
			return HttpResponseRedirect(reverse('profile'))
		else:
			messages.warning(request, 'Account not updated correctly!')
	if request.method == 'POST' and 'pass_reset' in request.POST:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		pass_form = PasswordChangeForm(user=request.user, data=request.POST)
		if pass_form.is_valid():
			pass_form.save()
			messages.success(request, 'Password was updated!')
			update_session_auth_hash(request, pass_form.user)
			return HttpResponseRedirect(reverse('profile'))
		else:
			messages.warning(request, 'Password was not updated')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
		pass_form = PasswordChangeForm(user=request.user)
	context = {
		'u_form': u_form,
		'p_form': p_form,
		'pass_form': pass_form,
	}
	return render(request, 'users/profile.html', context)

def UserProfile(request, pk=None):
	user = User.objects.get(pk=pk)
	if request.user.membership.team == user.membership.team:
		return render(request, 'users/user_profile.html', {'user': user})
	else:
		return HttpResponse('<h1>Not authorized to view this page</h1>')
# class TeamCreateView(LoginRequiredMixin, CreateView):
# 	model = Team
# 	fields = ['name', 'pin']


def TeamList(request):
	role = request.user.membership.role
	team = request.user.membership.team
	members = team.members.all()
	if role == 'Admin':
		projects = team.project_set.all().order_by('-date_created')
	else:
		projects = team.project_set.filter(members=request.user).order_by('-date_created')

	query = request.GET.get('query')
	if request.method == 'POST' and 'project_create' in request.POST:
		form = ProjectCreateForm(request.POST)
		update_form = TeamUpdateForm(instance=team)
		if form.is_valid():
			form.instance.team = request.user.membership.team
			form.save()
			return HttpResponseRedirect(reverse('team-list'))
	elif request.method == 'POST' and 'team_update' in request.POST:
		form = ProjectCreateForm()
		update_form = TeamUpdateForm(request.POST, instance=team)
		if update_form.is_valid():
			update_form.save()
			return HttpResponseRedirect(reverse('team-list'))
	else:
		form = ProjectCreateForm()
		update_form = TeamUpdateForm(instance=team)

	if query != None:
		projects = projects.filter(name__contains=query)
	if query == '':
		if role == 'Admin':
			projects = team.project_set.all().order_by('-date_created')
		else:
			projects = team.project_set.filter(members=request.user).order_by('-date_created')
	paginator = Paginator(projects, 12)
	page_number = request.GET.get('page')
	projects = paginator.get_page(page_number)
	return render(request, 'users/teaminfo.html', {'team': team, 'members': members, 'projects': projects, 'form': form, 'update_form': update_form, 'query': query})
	
def MembersList(request):
	members = request.user.membership.team.members.all()
	query = request.GET.get('query')
	if query != None:
		members = members.filter(Q(username__contains=query) | Q(email__contains=query))
	if query == '':
		members = request.user.membership.team.members.all()
	return render(request, 'users/members_list.html', {'members': members})


# def TeamJoin(request):	
# 	if request.method == 'POST':
# 		if Team.objects.filter(name=request.POST.get('team_name')).count() == 0:
# 			messages.warning(request, 'Invalid Team Name')
# 		else:
# 			team = Team.objects.get(name=request.POST.get('team_name'))
# 			if int(request.POST.get('pin')) == int(team.pin):
# 				instance = Membership(user=request.user, team=team)
# 				instance.save()
# 				messages.success(request, 'Team Joined')
# 				return redirect('home')
# 			else:
# 				messages.warning(request, 'Invalid Pin')

# 	return render(request, 'users/teamjoin.html')

class MembershipUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Membership
	fields = ['role']

	def get_success_url(self):
		return reverse('team-list')

	def test_func(self):
		if self.request.user.membership.role == 'Admin':
			team = self.get_object().team
			print(team)
			print(self.request.user.membership.team)
			if self.request.user.membership.team == team:
				return True
			return False
		return False

class MembershipDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Membership

	def get_success_url(self):
		return reverse('team-list')
	
	def test_func(self):
		if self.request.user.membership.role == 'Admin':
			team = self.get_object().team
			if self.request.user.membership.team == team:
				return True
			return False
		return False


