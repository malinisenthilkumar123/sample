from django.urls import path
from . import views
from .views import LoanedBooksListView  # ✅ Correctly imported

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    
    # ✅ Use only LoanedBooksListView
    path('mybooks/', LoanedBooksListView.as_view(), name='my-borrowed'),
]
