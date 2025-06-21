from django.contrib import admin
from .models import Item, CartItem, Purchase

admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(Purchase)
