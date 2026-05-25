from django.contrib import admin
from .models import Ticket, Book

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
admin.site.register(Ticket)
