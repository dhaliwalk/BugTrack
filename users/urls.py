from django.urls import path
from . import views as user_views
from .views import MembershipUpdateView, MembershipDeleteView
urlpatterns = [
    # path('new/', user_views.TeamCreateView.as_view(), name='team-create'),
    path('list/', user_views.TeamList, name='team-list'),
    path('members/', user_views.MembersList, name='members-list'),
    path('<int:pk>/user/profile/', user_views.UserProfile, name='user-profile'),
    # path('join/', user_views.TeamJoin, name='team-join'),
    path('<int:pk>/membership/update/', MembershipUpdateView.as_view(), name='membership-update'),
    path('<int:pk>/membership/delete/', MembershipDeleteView.as_view(), name='membership-delete'),
]
