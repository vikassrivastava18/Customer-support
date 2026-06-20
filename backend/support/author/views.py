from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
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
    serializer_class = TicketCreateSerializer
    queryset = Ticket.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        isbn = serializer.validated_data["isbn"]
        query = serializer.validated_data["query"]

        book = get_object_or_404(Book, isbn=isbn)

        graph = build_graph()
        result = graph.invoke({
            "book": isbn,
            "messages": [HumanMessage(content=query)],
        })

        response_text = result["messages"][-1].content

        ticket = Ticket.objects.create(
            query=query,
            book=book,
            response=response_text,
        )

        return Response(
            {
                "id": ticket.id,
                "query": ticket.query,
                "response": ticket.response,
            },
            status=status.HTTP_201_CREATED,
        )


class ChatView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def post(self, request):
        query = request.data.get("query")
        session_id = request.user.username
        config = {
            "configurable": {
                "thread_id": session_id
            }
        }
        print("config: ", config)
        graph = build_graph()
        result = graph.invoke({
            "messages": [HumanMessage(content=query)],
        }, config=config)
        print("Messages: ", result["messages"])
        response = result["messages"][-1].content

        return Response(response, status=status.HTTP_200_OK)

