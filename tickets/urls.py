from django.urls import path
from . import views
from .views import TicketCreateView, TicketUpdateView, TicketDeleteView, CommentCreateView, CommentUpdateView, CommentDeleteView

urlpatterns = [
    path('<int:pk>/info/', views.TicketInfo, name='ticket-info'),
    path('<int:pk>/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    path('<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/comment/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/comment/delete/', CommentDeleteView.as_view(), name='comment-delete'),
]