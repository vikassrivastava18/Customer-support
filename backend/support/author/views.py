from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import BookSerializer
from .models import Book
# Create your views here.


class BookListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BookSerializer

    def get_queryset(self):
        # Return only books for the authenticated user
        return (Book.objects.filter(author=self.request.user)
                )