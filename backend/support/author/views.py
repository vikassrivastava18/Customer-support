from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from langchain_core.messages import HumanMessage

from .serializers import (BookSerializer,
                          TicketListSerializer,
                          TicketCreateSerializer)
from .models import Book, Ticket
from utils.graph import Graph
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
            Q(book__author=self.request.user) |
            Q(user=self.request.user)
        )


class TicketCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    serializer_class = TicketCreateSerializer
    queryset = Ticket.objects.all()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            isbn = serializer.validated_data["isbn"]
            query = serializer.validated_data["query"]
            book = get_object_or_404(Book, isbn=isbn)

            graph = Graph.build_graph()
            session_id = request.user.username
            config = {
                "configurable": {
                    "thread_id": session_id
                }
            }
            result = graph.invoke({
                "book": isbn,
                "messages": [HumanMessage(content=query)],
            }, config=config)

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
        except Exception as e:
            return Response(
                    {"error": str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
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
        graph = Graph.build_graph()
        result = graph.invoke({
            "messages": [HumanMessage(content=query)],
            "username": session_id
        }, config=config)
        response = result["messages"][-1].content

        return Response(response, status=status.HTTP_200_OK)

