from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, UpdateView
from .models import Profile, Team
from projects.models import Project

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

class TeamUpdateForm(forms.ModelForm):
	class Meta:
		model = Team
		fields = ['name', 'description', 'pin']


class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields =  ['image']

class TeamCreationForm(forms.ModelForm):
	class Meta:
		model = Team
		fields =  ['name', 'description', 'pin']

class TeamJoinForm(forms.Form):
	team_name = forms.CharField(max_length=128)
	team_pin = forms.IntegerField()


class ProjectCreateForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ['name', 'description']