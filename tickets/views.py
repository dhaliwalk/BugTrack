from django.shortcuts import render
from .models import Ticket 

def TicketInfo(request, pk=None):
	if pk:
		ticket = Ticket.objects.get(pk=pk)
	comments = ticket.comment_set.all()
	return render(request, 'tickets/ticket_info.html', {'comments': comments, 'ticket':ticket})