from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('books/', views.authors, name="books_list"),
]
