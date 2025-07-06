from django.shortcuts import render

from store.models import Product, ShoppingCart

def index(request):
    #This view displays the product listing page.
    context = {
        'products': Product.objects.all(),
    }
    return render(request, 'store/product_list.html', context)

def show(request, id):
    #This view displays the details of a single product.
    context = {
        'product': Product.objects.get(id=id),
    }
    return render(request, 'store/product.html', context)

def cart(request):
    #This view shows a shopping cart page.
    context = {
        'items': [],
        'subtotal': 1.0,
        'tax_rate': int(ShoppingCart.TAX_RATE * 100.0),
        'tax_total': 2.0,
        'total': 3.0,
    }
    return render(request, 'store/cart.html', context)
