from django.db.models import Avg
from django.shortcuts import render

from .models import Author


def home(request):
    return render(request, 'books_temp/home.html')


def authors(request):
    author = Author.objects.prefetch_related('book_set__authors')
    average_rating = Author.objects.aggregate(avg_rating=Avg('book__rating'))
    context = {'authors': author, 'average_rating': average_rating['avg_rating']}
    return render(request, 'books_temp/authors_list.html', context)
