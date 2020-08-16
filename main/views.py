from django.shortcuts import render
from users.models import Team

Group = Team.objects.get(name='cool').members.all()
def home(request):
	return render(request, 'main/base.html')


