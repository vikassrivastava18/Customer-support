from rest_framework import serializers
from .models import Book, Ticket


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title', read_only=True)
    class Meta:
        model = Ticket
        fields = ['query', 'book']


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['query', 'book']
