from django.urls import path
from . import views

urlpatterns = [
    path('<int:pk>/info/', views.TicketInfo, name='ticket-info'),
]