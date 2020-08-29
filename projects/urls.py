from django.urls import path
from . import views
from .views import ProjectUpdateView, ProjectDeleteView, ProjectMemberCreateView, ProjectMemberDeleteView

urlpatterns = [
    path('list/', views.list, name='project-list'),
    # path('<int:pk>/join/', views.ProjectJoin, name='project-join'),
    path('<int:pk>/info/', views.ProjectInfo, name='project-info'),
    # path('new/', ProjectCreateView.as_view(), name='project-create'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project-update'),
    path('<int:pk>/delete/', ProjectDeleteView.as_view(), name='project-delete'),
    path('<int:pk>/ProjectMember/new/', ProjectMemberCreateView.as_view(), name='projectmember-create'),
    path('<int:pk>/ProjectMember/delete/', ProjectMemberDeleteView.as_view(), name='projectmember-delete'),
]