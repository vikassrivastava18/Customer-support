from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.response import Response
from langchain_core.messages import HumanMessage

from .serializers import (BookSerializer,
                          TicketListSerializer,
                          TicketCreateSerializer)
from .models import Book, Ticket
from staff.graph import build_graph


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

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            book_id, query = request.data.get("book"), request.data.get("query")
            book = Book.objects.get(id=book_id)
            graph = build_graph()
            s = {
                "book": book_id,
                "messages": [HumanMessage(content=query)]
            }
            result = graph.invoke(s)
            response = result["messages"][-1].content
            Ticket.objects.create(query=query,
                                  book=book,
                                  response=response)
            # serializer.save(book=request.data.get("book"))  # example
            return Response(serializer.data, status=status.HTTP_201_CREATED)