from django.urls import path
from . import views
from .views import ProjectCreateView

urlpatterns = [
    path('list/', views.list, name='project-list'),
    path('<int:pk>/join/', views.ProjectJoin, name='project-join'),
    path('new/', ProjectCreateView.as_view(), name='project-create'),
]