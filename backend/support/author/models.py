from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


# Create your models here.
class GenreType(models.TextChoices):
    FANTACY = 'fa', _('Fantacy')
    FICTION = 'fi', _('Fiction')
    ROMANCE = 'ro', _('Romance')


class BookStatusType(models.TextChoices):
    PUBLISHED = 'pu', _('Published')
    REVIEW = 're', _('Review')


class Book(models.Model):
    """
    An author published books with key details: title, ISBN, genre,
    publication date, status, MRP, total copies sold, total royalty earned,
    royalty paid, and royalty pending.
    """
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=128)
    isbn = models.CharField(max_length=13)
    genre = models.CharField(
        max_length=2,
        choices=GenreType.choices,
        default=GenreType.FICTION
    )
    pub_date = models.DateField()
    status = models.CharField(
        max_length=2,
        choices=BookStatusType.choices,
        default=BookStatusType.REVIEW
    )
    mrp = models.IntegerField()
    copies_sold = models.IntegerField(default=0)
    royality_earned = models.IntegerField(default=0)
    royality_paid = models.IntegerField(default=0)
    royality_pending = models.IntegerField(default=0)


    def __str__(self) -> str:
        return f'{self.title} - {self.status}'
    

class TicketStatus(models.TextChoices):
    OPEN = 'op', _('Open')
    PROGRESS = 'pr', _('In-progress')
    RESOLVED = 're', _('Resolved')
    CLOSED = 'cl', _('Closed')


class Ticket(models.Model):
    """
    Tickets the author has submitted, with current status (Open, In
    Progress, Resolved, Closed), the original query, and any responses from the admin team.   
    """
    query = models.CharField(max_length=512)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=2,
        choices=TicketStatus.choices,
        default=TicketStatus.PROGRESS
    )
    response = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.book.title}, Query: {self.query}, Status: {self.status}'
    
