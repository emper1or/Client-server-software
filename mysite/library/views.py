from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import BookForm, BookCoverForm
from .models import Author, Book, BookCover


@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')
        if name:  # Проверяем, что имя автора указано
            Author.objects.create(name=name, bio=bio)
            return redirect('add_book')  # Перенаправляем на страницу добавления книги
    return render(request, 'add_author.html')


@login_required
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

            # Добавляем текущего пользователя к книге
            book.users.add(request.user)

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


@login_required
def success(request):
    return render(request, 'success.html')

@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, id=pk)
    covers = BookCover.objects.filter(book=book)
    return render(request, 'book_detail.html', {'book': book, 'covers': covers})

@login_required
def edit_book(request, pk):
    book = get_object_or_404(Book, id=pk)

    # Получаем первую обложку книги (если она существует)
    book_cover = book.bookcover_set.first()

    if request.method == 'POST':
        book_form = BookForm(request.POST, instance=book)
        cover_form = BookCoverForm(request.POST, request.FILES, instance=book_cover)

        if book_form.is_valid() and cover_form.is_valid():
            book_form.save()

            # Если у книги уже есть обложка, удаляем её файл
            if 'cover' in cover_form.changed_data:
                covers = BookCover.objects.filter(book=book)
                for cover in covers:
                    cover.cover.delete()
                    cover.delete()

            # Сохраняем новую обложку
            cover = cover_form.save(commit=False)
            cover.book = book  # Связываем обложку с книгой
            cover.save()

            return redirect('book_detail', pk=book.id)
    else:
        book_form = BookForm(instance=book)
        cover_form = BookCoverForm(instance=book_cover)

    return render(request, 'edit_book.html', {
        'book_form': book_form,
        'cover_form': cover_form,
        'book': book,
    })
@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, id=pk)
    if request.method == 'POST':
        covers = BookCover.objects.filter(book=book)
        for cover in covers:
            cover.cover.delete()
            cover.delete()
        book.delete()
        return redirect('dashboard')
    return render(request, 'delete_book.html', {'book': book})
