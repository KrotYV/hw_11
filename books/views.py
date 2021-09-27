from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView

from .models import Author, Book, Publisher, Store


def authors(request):
    author = Author.objects.prefetch_related('book_set__authors')
    average_rating = Author.objects.aggregate(avg_rating=Avg('book__rating'))
    context = {'authors': author, 'average_rating': average_rating['avg_rating']}
    return render(request, 'books_temp/authors_list.html', context)


def publishers(request):
    publishers = Publisher.objects.all().annotate(num_books=Count('book'))
    return render(request, 'books_temp/publishers.html', {'publishers': publishers})


def stores(request):
    stores = Store.objects.all().annotate(num_books=Count('books'))
    return render(request, 'books_temp/stores.html', {'stores': stores})


def authors_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    books = Book.objects.select_related('publisher')
    return render(request, 'books_temp/authors_inf.html', {'author': author, 'books': books})


class HomePageView(TemplateView):
    template_name = 'books_temp/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['num_books'] = Book.objects.count()
        context['num_authors'] = Author.objects.count()
        context['num_publishers'] = Publisher.objects.count()
        context['num_stores'] = Store.objects.count()
        return context


class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    template_name = 'books_temp/new_book.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_url = reverse_lazy('books')
    login_url = '/admin/login/'


class BookUpdate(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Book
    template_name = 'books_temp/book_update.html'
    fields = ['name', 'pages', 'price', 'rating', 'authors', 'publisher', 'pubdate']
    success_message = "Book updated!"
    login_url = '/admin/login/'
    redirect_field_name = 'admin'

    def get_success_url(self):
        book_id = self.kwargs['pk']
        return reverse_lazy('book-update', kwargs={'pk': book_id})


class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books_temp/book_delete.html'
    success_url = reverse_lazy('books')
    login_url = '/admin/login/'


class BookDetail(DetailView):
    model = Book
    template_name = 'books_temp/books_inf.html'


class BookList(ListView):
    model = Book
    template_name = 'books_temp/books_list.html'
    paginate_by = 10
    queryset = Book.objects.annotate(num_authors=Count('authors')).select_related('publisher')
    context_object_name = 'books'
