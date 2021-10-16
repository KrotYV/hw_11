from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='index'),

    path('authors/', views.authors, name='authors'),
    path('authors/<int:pk>/', views.authors_detail, name='authors_detail'),

    path('publishers/', views.publishers, name='publishers'),
    path('stores/', views.stores, name='stores'),

    path('book/create/', views.BookCreate.as_view(), name='book-create'),
    path('book/update/<int:pk>/', views.BookUpdate.as_view(), name='book-update'),
    path('book/delete/<int:pk>/', views.BookDelete.as_view(), name='book-delete'),
    path('books/<int:pk>/', views.BookDetail.as_view(), name='books_detail'),
    path('books/', views.BookList.as_view(), name='books'),
]
