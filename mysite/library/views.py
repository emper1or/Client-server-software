from django.shortcuts import render, redirect
from .forms import AuthorForm, BookForm, BookCoverForm
from .models import Author, Book, BookCover


def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        if name:  # Проверяем, что имя автора указано
            Author.objects.create(name=name, bio=bio)
            return redirect('add_book')  # Перенаправляем на страницу добавления книги
    return render(request, 'add_author.html')


def add_book(request):
    authors = Author.objects.all()

    if request.method == 'POST':
        book_form = BookForm(request.POST)
        cover_form = BookCoverForm(request.POST, request.FILES)

        if book_form.is_valid() and cover_form.is_valid():
            # Сохраняем книгу, связывая с автором
            book = book_form.save(commit=False)
            book.author = book_form.cleaned_data['author']
            book.save()

            # Сохраняем обложку, связывая с книгой
            cover = cover_form.save(commit=False)
            cover.book = book
            cover.save()

            return redirect('success')  # Перенаправление на страницу успеха
    else:
        book_form = BookForm()
        cover_form = BookCoverForm()

    return render(request, 'add_book.html', {
        'book_form': book_form,
        'cover_form': cover_form,
        'authors': authors,
    })


def success(request):
    return render(request, 'success.html')