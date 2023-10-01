from django.urls import path
from . import views

urlpatterns = [
    path('my_books/', views.UserBooksView.as_view(), name='my-book-list'),
    path('books/', views.BooksView.as_view(), name='my-book-list'),
    path('books/favorite/', views.FavoriteBookView.as_view(), name='favorites'),
]
