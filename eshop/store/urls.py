from django.urls import path
from . import views

urlpatterns = [
    path("", views.item_list, name="item_list"),
    path("cart/", views.cart_view, name="cart"),
    path("buy/", views.buy_items, name="buy"),
    path("add/<int:item_id>/", views.add_to_cart, name="add_to_cart"),
    path("signup/", views.signup, name="signup"),
]
