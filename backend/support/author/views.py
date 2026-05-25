from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from .serializers import (BookSerializer,
                          TicketListSerializer,
                          TicketCreateSerializer)
from .models import Book, Ticket
# Create your views here.

class BookListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.filter(author=self.request.user)


class TicketListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer

    def get_queryset(self):
        return Ticket.objects.filter(
            book__author=self.request.user
        )


class TicketCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Ticket.objects.all()
    serializer_class = TicketCreateSerializer

    def get_queryset(self):
        return Ticket.objects.filter(
            book__author=self.request.user
        )


