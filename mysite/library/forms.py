from django import forms
from .models import Author, Book, BookCover


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'bio']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'description', 'author']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].required = False


class BookCoverForm(forms.ModelForm):
    class Meta:
        model = BookCover
        fields = ['cover']
