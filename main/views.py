from django.shortcuts import render
from users.models import Team
from users.views import register
Group = Team.objects.get(name='cool').members.all()
def home(request):
	if request.user.is_authenticated:
		return render(request, 'main/base.html')
	else:
		return register(request)
	


