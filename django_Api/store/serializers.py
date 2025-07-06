from rest_framework import serializers
from store.models import Product, ShoppingCartItem

"""
In Django REST Framework (DRF), serializers are responsible for converting 
complex data types—like Django models—into Python datatypes that can then be easily converted to JSON, XML, etc., for use in APIs. 
They also handle the reverse: 
converting incoming JSON data into validated Python objects (and optionally saving them to the database).
"""

class CartItemSerializer(serializers.ModelSerializer):
    """"
    It ensures that when cart items are created or updated, the quantity must be between 1 and 100.
    The product is probably a ForeignKey to the Product model.
    """
    quantity = serializers.IntegerField(min_value=1, max_value=100)  # Ensure quantity is at least 1
    class Meta:
        model = ShoppingCartItem
        fields = ('product', 'quantity')


class ProductStatSerializer(serializers.Serializer):
    """"
    This is not tied to a Django model (notice it inherits from serializers.Serializer, not ModelSerializer).
    stats is expected to look something like:
    {
        "stats": {
            "views": [100, 200],
            "purchases": [5, 10]
        }
    }
    """
    stats = serializers.DictField(
        child=serializers.ListField(
            child=serializers.IntegerField()
        )
    )

class ProductSerializer(serializers.ModelSerializer):
    is_on_sale = serializers.BooleanField(read_only=True)
    current_price = serializers.FloatField(read_only=True)
    description = serializers.CharField(min_length=2, max_length=500)
    cart_items = serializers.SerializerMethodField()  
    #price = serializers.FloatField(min_value=1.0, max_value = 100)  #The FloatField is used for the current price that's calculated by a method in the Product model, it could be the price or sale price
    price = serializers.DecimalField(
        min_value=1.00, max_value=100000,
        max_digits=None, decimal_places=2,
    ) # The DecimalField used for the price is not calculated, it's the price set for the Product. 
    sale_start = serializers.DateTimeField(
        required=False,  # This field is optional
        input_formats=['%I:%M %p %d %B %Y'], format=None,
        allow_null=True, 
        help_text='Accepted format is "12:01 PM 16 April 2025',
        style ={'input_type': 'text', 'placeholder': '12:01 PM 16 June 2025'}
    )  
    sale_end = serializers.DateTimeField(
        required=False,  # This field is optional
        input_formats=['%I:%M %p %d %B %Y'], format=None,
        allow_null=True, 
        help_text='Accepted format is "12:01 PM 16 April 2025',
        style ={'input_type': 'text', 'placeholder': '12:01 PM 16 June 2025'}
    ) 
    photo = serializers.ImageField(default=None)
    warranty = serializers.FileField(write_only= True,  default=None)

    class Meta:
        model = Product # The model we are serializing
        fields = ('id', 'name', 'description', 'price', 'sale_start', 'sale_end',
                  'is_on_sale', 'current_price', 'cart_items', 'photo', 'warranty') # Which fields to include in the JSON output.

    def get_cart_items(self, instance):
        items = ShoppingCartItem.objects.filter(product=instance)
        return CartItemSerializer(items, many=True).data

    def update(self, instance, validated_data):
        if validated_data.get('warranty', None):
            instance.description += '\n\nWarranty Information:\n'
            instance.description += b'; '.join(
                validated_data['warranty'].readlines()
            ).decode()
        return super().update(instance, validated_data) #this save the object after update
    
    def create(Self, validated_data):
        validated_data.pop('warranty')  # Remove warranty from validated_data if it exists
        return Product.objects.create(**validated_data)
    
    # def to_representation(self, instance):
    #     #It overrides the default behavior to include extra calculated fields.
    #     data = super().to_representation(instance)
    #     data['is_on_sale'] = instance.is_on_sale()
    #     data['current_price'] = instance.current_price()
    #     return data
    

"""
(.venv) ➜  online_store git:(main) ✗ ./manage.py shell
9 objects imported automatically (use -v 2 for details).

Python 3.11.7 (main, Dec 15 2023, 12:09:04) [Clang 14.0.6 ] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import json
>>> from store.models import *
>>> from store.serializers import *
>>> product = Product.objects.all().first()
>>> cart = ShoppingCart()
>>> cart.save()
>>> item = ShoppingCartItem(shopping_cart=cart, product=product, quantity=5)
>>> item.save()
>>> serializer = ProductSerializer(product)
>>> print(json.dump(serializer.data, indent=2))

"""