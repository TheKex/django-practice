from django.shortcuts import render
from django.db.models import Max, Min
from .models import Book


def books_view(request):
    template = 'books/books_list.html'
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, template, context)


def books_pub_date_view(request, pub_date):
    template = 'books/books_list.html'

    books = Book.objects.filter(pub_date=pub_date)
    next_date = Book.objects.filter(pub_date__gt=pub_date).aggregate(Min('pub_date'))['pub_date__min']
    prev_date = Book.objects.filter(pub_date__lt=pub_date).aggregate(Max('pub_date'))['pub_date__max']
    context = {
        'books': books,
        'next_date': next_date,
        'prev_date': prev_date,
    }
    return render(request, template, context)
