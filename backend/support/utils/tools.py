from django.shortcuts import get_object_or_404
from author.models import Book


# Define the tools
class Tools:
    @staticmethod
    def get_royality_earned(isbn):
        """Get the royality earning for a book."""
        book = get_object_or_404(Book, isbn=isbn)
        return book.royality_earned

    @staticmethod
    def get_royality_paid(isbn):
        """Get the royality pending for a book.."""
        book = get_object_or_404(Book, isbn=isbn)
        return book.royality_earned

    @staticmethod
    def get_royality_pending(isbn):
        """Get the royality pending for a book."""
        book = get_object_or_404(Book, isbn=isbn)
        return book.royality_pending

    @staticmethod
    def get_book_publish_status(isbn):
        """Get a book current live status
        """
        from datetime import date
        book = get_object_or_404(Book, isbn=isbn)
        return f"Already published on {book.pub_date}" if book.pub_date < date.today() \
            else (f"Not published yet, "
                  f"publication date: {book.pub_date}")

    @staticmethod
    def get_tools():
        tools = [Tools.get_royality_earned, Tools.get_royality_paid,
                 Tools.get_royality_pending, Tools.get_book_publish_status]
        return tools