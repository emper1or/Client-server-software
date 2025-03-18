from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect
from django.shortcuts import render
from library.models import Book, BookCover

from .forms import RegisterForm


def anonymous_required(user):
    return not user.is_authenticated


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


@user_passes_test(anonymous_required, login_url='home')
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Неверное имя пользователя или пароль'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def dashboard(request):
    user = request.user
    books = Book.objects.filter(users=user)  # Получаем книги пользователя
    covers = BookCover.objects.filter(book__in=books)  # Получаем обложки для этих книг

    context = {
        'user': user,
        'books': books,
        'covers': covers,
    }
    return render(request, 'dashboard.html', context)


def home(request):
    return render(request, 'home.html')
