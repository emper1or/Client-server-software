from django.contrib import admin
from .models import BookCover, Book, Author

admin.site.register(BookCover)
admin.site.register(Book)
admin.site.register(Author)

# Register your models here.
