from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, TeamJoinForm, TeamCreateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Team, Membership
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse

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

def RegisterUserCreateTeam(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		form_t = TeamCreateForm(request.POST)
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
		form_t = TeamJoinForm()
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


class TeamCreateView(LoginRequiredMixin, CreateView):
	model = Team
	fields = ['name', 'pin']


def TeamList(request):
	team = request.user.team_set.first()
	members = team.members.all()
	return render(request, 'users/teaminfo.html', {'teams': team, 'members': members})


def TeamJoin(request):	
	if request.method == 'POST':
		if Team.objects.filter(name=request.POST.get('team_name')).count() == 0:
			messages.warning(request, 'Invalid Team Name')
		else:
			team = Team.objects.get(name=request.POST.get('team_name'))
			if int(request.POST.get('pin')) == int(team.pin):
				instance = Membership(user=request.user, team=team)
				instance.save()
				messages.success(request, 'Team Joined')
				return redirect('home')
			else:
				messages.warning(request, 'Invalid Pin')

	return render(request, 'users/teamjoin.html')

class MembershipUpdateView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
	model = Membership
	fields = ['role']

	def get_success_url(self):
		return reverse('team-list')

	def test_func(self):
		if self.request.user.membership.role == 'admin':
			return True
		return False

class MembershipDeleteView(UserPassesTestMixin, LoginRequiredMixin, DeleteView):
	model = Membership

	def get_success_url(self):
		return reverse('team-list')
	
	def test_func(self):
		if self.request.user.membership.role == 'admin':
			return True
		return False


