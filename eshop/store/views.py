from django.shortcuts import render, redirect, get_object_or_404
from .models import Item, CartItem, Purchase
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("item_list")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})


def item_list(request):
    items = Item.objects.all()
    return render(request, "store/item_list.html", {"items": items})


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, item=item)
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect("cart")


@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, "store/cart.html", {"cart_items": cart_items})


@login_required
def buy_items(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if cart_items.exists():
        purchase = Purchase.objects.create(user=request.user)
        purchase.items.set(cart_items)
        cart_items.delete()  # Clear cart
    return redirect("item_list")
