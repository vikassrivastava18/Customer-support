from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from author.models import Book, Ticket
from .serializers import (TicketListSerializer,
                          TicketUpdateSerializer)

# Create your views here.

class TicketListView(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Ticket.objects.all()
    serializer_class = TicketListSerializer


class TicketUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    queryset = Ticket.objects.all()
    serializer_class = TicketUpdateSerializer


