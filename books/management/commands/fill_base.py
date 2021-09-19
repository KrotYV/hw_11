import random

from books.models import Author, Book, Publisher, Store

from django.core.management.base import BaseCommand

from faker import Faker
fake = Faker()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('count', type=int, choices=range(1, 1000), help='Number of records for Author and Publisher'
                                                                            '(from 1 to 1000)')

    def handle(self, *args, **options):
        count = options['count']

        for i in range(count):
            Author.objects.create(name=fake.name(), age=fake.random_int(min=15, max=99))

        for i in range(count):
            Publisher.objects.create(name=fake.company())

        for el in Publisher.objects.all():
            for i in range(3):
                Book.objects.create(name=fake.sentence(nb_words=4), pages=fake.random_int(min=100, max=800),
                                    price=fake.pydecimal(right_digits=2, min_value=10, max_value=800),
                                    rating=fake.pyfloat(right_digits=1, min_value=0, max_value=10),
                                    publisher=el, pubdate=fake.date())

        for i in range(round(count/2)):
            books = Book.objects.all()
            store = Store.objects.create(name=fake.company())
            id_ = books[:fake.random_int(min=1, max=len(books))]
            random.shuffle(id_)
            store.books.set(id_)

        list_book_id = list(Book.objects.values_list('id', flat=True))
        list_author_id = list(Author.objects.values_list('id', flat=True))

        for book_el in list_book_id:
            authors_list = list()
            random.shuffle(list_author_id)
            book_authors_id = list_author_id[:fake.random_int(min=1, max=len(list_author_id))]

            for author_el in book_authors_id:
                authors_list.append(Book.authors.through(book_id=book_el, author_id=author_el))
            Book.authors.through.objects.bulk_create(authors_list)

        self.stdout.write(self.style.SUCCESS('Successfully filled database'))
