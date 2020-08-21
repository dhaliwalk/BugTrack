from django.contrib import admin
from .models import Ticket, Comment, History

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(History)