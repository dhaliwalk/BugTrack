from django.contrib import admin
from .models import Ticket, Comment, History, Attachment

admin.site.register(Ticket)
admin.site.register(Comment)
admin.site.register(History)
admin.site.register(Attachment)