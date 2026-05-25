from rest_framework import serializers
from author.models import Book, Ticket


class TicketListSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source='book.title', read_only=True)
    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )
    class Meta:
        model = Ticket
        fields = ['id','query', 'book', 'status_display', 'response']


class TicketUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['query', 'id', 'response', 'status']