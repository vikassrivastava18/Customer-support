from django.urls import path
from .views import (BookListView,
                    CreateListTicketView)

urlpatterns = [
    path('books', BookListView.as_view(), name='books'),
    path('tickets', CreateListTicketView.as_view(), name='create_ticket')
]
