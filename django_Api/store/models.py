
from django.utils import timezone
from django.db import models

""""
Class	            Role
Product	            Holds product data, price, discount
ShoppingCart	    Represents a user’s cart
ShoppingCartItem	Links products and quantities to cart


Imagine the database like this:

ShoppingCart    id	    name	    address
cart1	        1	    "Kostas"	"Athens, GR"

Product	    id	    name	    price
prod1	    1	    "iPhone"	799.0
prod2	    2	    "MacBook"	1299.0

ShoppingCartItem	id	    shopping_cart (FK)	product (FK)	quantity
item1	            1	    cart1	            prod1	           2
item2	            2	    cart1	            prod2	           1
"""

class Product(models.Model):
    DISCOUNT_RATE = 0.10

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    sale_start = models.DateTimeField(blank=True, null=True, default=None)
    sale_end = models.DateTimeField(blank=True, null=True, default=None)
    photo = models.ImageField(blank=True, null=True, default=None, upload_to='products')

    def is_on_sale(self):
        now = timezone.now()
        if self.sale_start:
            if self.sale_end:
                return self.sale_start <= now <= self.sale_end
            return self.sale_start <= now
        return False

    def get_rounded_price(self):
        return round(self.price, 2)

    def current_price(self):
        if self.is_on_sale():
            discounted_price = self.price * (1 - self.DISCOUNT_RATE)
            return round(discounted_price, 2)
        return self.get_rounded_price()

    def __repr__(self):
        return '<Product object ({}) "{}">'.format(self.id, self.name)

class ShoppingCart(models.Model):
    TAX_RATE = 0.13
  
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)

    def subtotal(self):
        amount = 0.0
        for item in self.items.all():
            amount += item.quantity * item.product.get_price()
        return round(amount, 2)

    def taxes(self):
        return round(self.TAX_RATE * self.subtotal(), 2)

    def total(self):
        return round(self.subtotal() + self.taxes(), 2)
 
    def __repr__(self):
        name = self.name or '[Guest]'
        address = self.address or '[No Address]'
        return '<ShoppingCart object ({}) "{}" "{}">'.format(self.id, name, address)

class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, related_name='items', related_query_name='item', on_delete=models.CASCADE) # This creates a many-to-one relationship with the ShoppingCart model.
    product = models.ForeignKey(Product, related_name='+', on_delete=models.CASCADE) # This links each ShoppingCartItem to a Product.
    quantity = models.IntegerField()

    def total(self):
        return round(self.quantity * self.product.current_price())

    def __repr__(self):
        return '<ShoppingCartItem object ({}) {}x "{}">'.format(self.id, self.quantity, self.product.name)
