from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_book, name='add_book'),
    path('add-author/', views.add_author, name='add_author'),
    path('success/', views.success, name='success'),
]