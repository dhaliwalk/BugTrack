from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TeamJoinForm, TeamCreationForm, ProjectCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Team, Membership
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.core.paginator import Paginator
from .decorators import unauthenticated_user

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
	if request.method == 'POST':
		u_form = UserUpdateForm(request.POST, instance=request.user)
		p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		
		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request, 'You account has been updated')
			return redirect('profile')

	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)
	context = {
		'u_form': u_form,
		'p_form': p_form
	}
	return render(request, 'users/profile.html', context)


# class TeamCreateView(LoginRequiredMixin, CreateView):
# 	model = Team
# 	fields = ['name', 'pin']


def TeamList(request):
	team = request.user.membership.team
	members = team.members.all()
	projects = team.project_set.all()

	paginator = Paginator(members, 5)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	if request.method == 'POST':
		form = ProjectCreateForm(request.POST)
		if form.is_valid():
			form.instance.team = request.user.membership.team
			form.save()
			return render(request, 'users/teaminfo.html', {'team': team, 'members': members, 'page_obj': page_obj, 'projects': projects, 'form': form})
	else:
		form = ProjectCreateForm()
	return render(request, 'users/teaminfo.html', {'team': team, 'members': members, 'page_obj': page_obj, 'projects': projects, 'form': form})
	



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


