from django.contrib import admin
from .models import Profile, Team, Membership

admin.site.register(Profile)
admin.site.register(Team)
admin.site.register(Membership)