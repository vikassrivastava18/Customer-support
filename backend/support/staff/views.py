import json
from pathlib import Path

from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User

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


class AddJsonDataView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Path to data.json
            file_path = Path(__file__).resolve().parent / "data.json"

            # Read JSON file
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            for author in data["authors"]:
                # Save the author and their books
                try:
                    user = User.objects.get(email=author["email"])
                except User.DoesNotExist:
                    username = "_".join(author["name"].split())
                    user = User.objects.create_user(
                        username=username,
                        email=author["email"],
                        password="hellYeah2020"
                    )

                for book in author["books"]:
                    Book.objects.create(author=user,
                                        title=book["title"],
                                        isbn=book["isbn"],
                                        genre=book["genre"],
                                        mrp=book["mrp"],
                                        royality_earned=book["author_royalty_per_copy"] or 0,
                                        royality_paid=book["royalty_paid"] or 0,
                                        royality_pending=book["royalty_pending"] or 0,
                                        pub_date=book["publication_date"])

            response_data = {
                "message": "JSON file loaded successfully",
                "data": data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except FileNotFoundError:
            return Response(
                {"error": "data.json file not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except json.JSONDecodeError:
            return Response(
                {"error": "Invalid JSON format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


