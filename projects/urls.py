from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.list, name='project-list'),
    path('<int:pk>/join/', views.ProjectJoin, name='project-join'),
]