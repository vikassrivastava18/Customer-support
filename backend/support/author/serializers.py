from rest_framework import serializers
from .models import Book, Ticket


class BookSerializer(serializers.ModelSerializer):
    genre_display = serializers.CharField(
        source='get_genre_display'
    )
    class Meta:
        model = Book
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    class Meta:
        model = Ticket
        fields = ['query', 'book', 'status_display', 'response']


class TicketCreateSerializer(serializers.ModelSerializer):
    isbn = serializers.CharField(write_only=True)

    class Meta:
        model = Ticket
        fields = ['query', 'isbn']

    def validate_isbn(self, value):
        try:
            Book.objects.get(isbn=value)
        except Book.DoesNotExist:
            raise serializers.ValidationError("Invalid ISBN")
        return value
