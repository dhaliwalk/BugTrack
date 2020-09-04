from django.contrib import admin
from .models import Project, ProjectMember, ProjectHistory

admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(ProjectHistory)