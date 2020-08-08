from django.urls import path
from . import views as user_views

urlpatterns = [
    path('new/', user_views.TeamCreateView.as_view(), name='team-create'),
    path('list/', user_views.TeamList, name='team-list'),
    path('<int:pk>/join/', user_views.TeamJoin, name='team-join'),
]
