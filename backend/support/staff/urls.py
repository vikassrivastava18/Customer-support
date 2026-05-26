from django.urls import path
from .views import (TicketUpdateView,
                    TicketListView,
                    AddJsonDataView)

urlpatterns = [
    path('tickets', TicketListView.as_view(), name='ticket_list'),
    path('tickets/<int:pk>', TicketUpdateView.as_view(), name='ticket_list'),
    path('add-data', AddJsonDataView.as_view(), name='add_data')
]
