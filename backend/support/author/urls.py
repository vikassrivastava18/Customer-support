from django.urls import path
from .views import (BookListView,
                    CreateTicketView)

urlpatterns = [
    path('books', BookListView.as_view(), name='books'),
    path('ticket', CreateTicketView.as_view(), name='create_ticket')
]
