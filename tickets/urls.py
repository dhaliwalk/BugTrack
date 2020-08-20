from django.urls import path
from . import views
from .views import TicketCreateView, CommentCreateView

urlpatterns = [
    path('<int:pk>/info/', views.TicketInfo, name='ticket-info'),
    path('<int:pk>/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
]