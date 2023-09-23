from django.shortcuts import render, redirect
from phones.models import Phone

def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort_order = request.GET.get('sort')
    phones = Phone.objects.all()
    if sort_order is not None:
        order = sort_order.replace('min_', '').replace('max_', '-')
        phones = phones.order_by(order).values()
    context = {
        'phones': phones,
    }
    return render(request, template, context)


def show_product(request, slug):
    template = 'product.html'
    phone = Phone.objects.filter(slug=slug).values()[0]
    context = {
        'phone': phone,
    }
    return render(request, template, context)
