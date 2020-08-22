from django.shortcuts import render
from users.models import Team
from users.views import RegisterUserJoinTeam

def home(request):
	if request.user.is_authenticated:
		return render(request, 'main/dashboard.html')
	else:
		return RegisterUserJoinTeam(request)
	


