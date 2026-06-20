from django.urls import path
from .views import (BookListView,
                    TicketCreateView,
                    TicketListView,
                    ChatView)

urlpatterns = [
    path('books', BookListView.as_view(), name='books'),
    path('tickets', TicketListView.as_view(), name='ticket_list'),
    path('create-ticket', TicketCreateView.as_view(), name='ticket_list'),
    path('author-chat', ChatView.as_view(), name='author_chat')
]
