from django.shortcuts import render
from users.models import Team
from users.views import RegisterUserJoinTeam
from tickets.models import Ticket
from django.db.models import Q

def home(request):
	context = {}
	if request.user.is_authenticated:
		tickets = Ticket.objects.filter(Q(submitter=request.user) | Q(developers=request.user)).distinct()
		context['ticket_high_count'] = tickets.filter(priority='High').count()
		context['ticket_medium_count'] = tickets.filter(priority='Medium').count()
		context['ticket_low_count'] = tickets.filter(priority='Low').count()
		context['ticket_none_count'] = tickets.filter(priority='None').count()
		context['ticket_open_progress_count'] = tickets.filter(status='Open').count()
		context['ticket_open_progress_count'] += tickets.filter(status='In Progress').count()
		context['ticket_closed_resolved_count'] = tickets.filter(status='Closed').count()
		context['ticket_closed_resolved_count'] += tickets.filter(status='Resolved').count()
		context['ticket_waiting_count'] = tickets.filter(status='Waiting on More Info').count()
		context['ticket_bug_count'] = tickets.filter(ticket_type='Bug').count()
		context['ticket_task_count'] = tickets.filter(ticket_type='Task').count()
		context['ticket_new_feature_count'] = tickets.filter(ticket_type='New Feature').count()
		context['ticket_improvement_count'] = tickets.filter(ticket_type='Improvement').count()
		return render(request, 'main/dashboard.html', context)
	else:
		return RegisterUserJoinTeam(request)
	
