from books.models import Author, Book, Publisher, Store

from django.contrib import admin


class BooksInstanceInline(admin.TabularInline):
    model = Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'age']
    list_filter = ['name', 'age']
    search_fields = ["name"]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'pages', 'price', 'rating', 'display_authors', 'publisher', 'pubdate']
    list_filter = ['name', 'rating', 'pubdate']
    search_fields = ["name"]


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ['name']
    inlines = [BooksInstanceInline]


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_books']
    list_filter = ['name']
