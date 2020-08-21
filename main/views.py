from django.shortcuts import render
from users.models import Team
from users.views import RegisterUserJoinTeam
Group = Team.objects.get(name='cool').members.all()
def home(request):
	if request.user.is_authenticated:
		return render(request, 'main/dashboard.html')
	else:
		return RegisterUserJoinTeam(request)
	


