from django.db import models
from accounts.models import CustomUser

class Author(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя автора")
    bio = models.TextField(verbose_name="Биография автора", blank=True, null=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название книги")
    description = models.TextField(verbose_name="Описание книги", blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Автор")
    users = models.ManyToManyField(CustomUser, related_name='books')

    def __str__(self):
        return self.title


class BookCover(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name="Книга")
    cover = models.ImageField(upload_to='covers/', verbose_name="Обложка книги")

    def __str__(self):
        return f"Обложка для {self.book.title}"
