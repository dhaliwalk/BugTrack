from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .models import Team, Membership

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, 'You account has been created you can now log in!')
			return redirect('login')
	else:
		form = UserRegisterForm()
	return render(request, 'users/register.html', {'form': form})


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


def TeamJoin(request, pk=None):
	if pk:
		team = Team.objects.get(pk=pk)
	if request.method == 'POST':
		if int(request.POST.get('pin')) == int(Team.objects.get(pk=pk).pin):
			instance = Membership(user=request.user, team=Team.objects.get(pk=pk))
			instance.save()
			return redirect('home')
		else:
			messages.warning(request, 'Invalid Pin')
	return render(request, 'users/teamjoin.html', {'team': team})


