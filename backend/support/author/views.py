from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BookSerializer, TicketCreateSerializer
from .models import Book, Ticket
# Create your views here.


class BookListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        # Return only books for the authenticated user
        return Book.objects.filter(author=self.request.user)


class CreateListTicketView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer

    def get_queryset(self):
        return Ticket.objects.filter(
            book__author=self.request.user
        )
    
