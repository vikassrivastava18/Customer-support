from django.urls import path
from .views import TicketUpdateView, TicketListView

urlpatterns = [
    path('tickets', TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>', TicketUpdateView.as_view(), name='ticket_list')
]
