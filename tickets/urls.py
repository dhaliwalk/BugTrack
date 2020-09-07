from django.urls import path
from . import views
from .views import (TicketCreateView, 
    TicketUpdateView, TicketDeleteView, 
    CommentUpdateView, 
    CommentDeleteView, 
    AttachmentUpdateView, AttachmentDeleteView, 
     TicketDevDeleteView)

urlpatterns = [
	path('', views.my_tickets, name='tickets'),
    path('<int:pk>/info/', views.TicketInfo, name='ticket-info'),
    path('<str:ticket_filter>/list/', views.TicketFilter, name='ticket-filter'),
    path('<int:pk>/new/', TicketCreateView.as_view(), name='ticket-create'),
    path('<int:pk>/update/', TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/delete/', TicketDeleteView.as_view(), name='ticket-delete'),
    # path('<int:pk>/comment/new/', CommentCreateView.as_view(), name='comment-create'),
    path('<int:pk>/comment/update/', CommentUpdateView.as_view(), name='comment-update'),
    path('<int:pk>/comment/delete/', CommentDeleteView.as_view(), name='comment-delete'),
    # path('<int:pk>/attachment/new/', AttachmentCreateView.as_view(), name='attachment-create'),
    path('<int:pk>/attachment/update/', AttachmentUpdateView.as_view(), name='attachment-update'),
    path('<int:pk>/attachment/delete/', AttachmentDeleteView.as_view(), name='attachment-delete'),
    # path('<int:pk>/TicketDev/new/', TicketDevCreateView.as_view(), name='ticketdev-create'),
    path('<int:pk>/TicketDev/delete/', TicketDevDeleteView.as_view(), name='ticketdev-delete'),
]