from django.contrib import admin
from .models import Ticket, Book

# Register your models here.
admin.site.register(Book)
admin.site.register(Ticket)
