from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .forms import BookForm, BookCoverForm
from .models import Author, Book, BookCover


@login_required
def add_author(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        bio = request.POST.get('bio')

        if name:
            Author.objects.create(name=name, bio=bio)
            messages.success(request, 'Автор успешно добавлен!')
            return redirect('add_book')  # Возвращаемся, данные книги уже сохранены

    return render(request, 'add_author.html')


@login_required
def add_book(request):
    authors = Author.objects.all()

    # Загружаем данные из сессии, если они есть
    initial_data = request.session.get('book_form_data', {})

    if request.method == 'POST':
        if 'add_author' in request.POST:
            # Сохраняем введённые данные в сессию перед переходом
            request.session['book_form_data'] = request.POST.dict()
            return redirect('add_author')

        book_form = BookForm(request.POST)
        cover_form = BookCoverForm(request.POST, request.FILES)

        if book_form.is_valid() and cover_form.is_valid():
            book = book_form.save(commit=False)
            book.author = book_form.cleaned_data['author']
            book.save()

            book.users.add(request.user)

            cover = cover_form.save(commit=False)
            cover.book = book
            cover.save()

            # Очищаем сохранённые данные после успешного добавления книги
            request.session.pop('book_form_data', None)

            messages.success(request, 'Книга успешно добавлена!')
            return redirect('dashboard')
    else:
        book_form = BookForm(initial=initial_data)
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
        messages.warning(request, f'Книга {book} успешно удалена!')
        return redirect('dashboard')
    return render(request, 'delete_book.html', {'book': book})
