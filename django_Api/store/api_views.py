from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView, \
    RetrieveUpdateDestroyAPIView, GenericAPIView #DestroyAPIView, UpdateAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from store.serializers import ProductSerializer, ProductStatSerializer
from store.models import Product


class ProductPagination(LimitOffsetPagination):
    """
    The ProductPagination class controls how many products are shown at a time in your API.
    """
    default_limit = 10 # By default, it shows 10 products.
    max_limit = 100 # A user can request more, but never more than 100.


class ProductList(ListAPIView):
    """
    API view to list all products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ('id',) # Filter products by ID
    search_fields = ('name', 'description') # Search products by name or description
    pagination_class = ProductPagination # Use the custom pagination class defined above

    def get_queryset(self): # Filter product on where the are on sale or not

        on_sale = self.request.query_params.get('on_sale', None) 
        if on_sale is None:
            return super().get_queryset()
        
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now
            )
        return queryset

        
class ProductCreate(CreateAPIView):
    """
    API view to create a new product.

    curls script
    curl -X POST http://127.0.0.1:8000/api/v1/products/new \
     -d "price=1.00" \
     -d "name=My product" \
     -d "description=Hello World"

    """
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get('price')
            if price is not None and float(price) <= 0:
                raise ValidationError("Price must be above $0.00.")
        except ValueError:
            raise ValidationError("Invalid price format. Please provide a valid number.")
        return super().create(request, *args, **kwargs)


# class ProductDestroy(DestroyAPIView):
#     """
#     API view to delete a product.
#     curl -X DELETE http://127.0.0.1:8000/api/v1/products/5/destroy
#     """
#     queryset = Product.objects.all()
#     lookup_field = 'id'

#     def delete(self, request, *args, **kwargs):
#         products_id = request.data.get('id')
#         response = super().delete(request, *args, **kwargs)
#         if response.status_code == 204: #product deleted successfully
#             from django.core.cache import cache
#             cache.delete(f'product_data_{products_id}') # Clear the cache for this product
#         return response

class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    API view to get, update or delete a product.
    curl -X GET http:// 
    """
    queryset = Product.objects.all()
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def delete(self, request, *args, **kwargs):
         products_id = request.data.get('id')
         response = super().delete(request, *args, **kwargs)
         if response.status_code == 204: #product deleted successfully
             from django.core.cache import cache
             cache.delete(f'product_data_{products_id}') # Clear the cache for this product
         return response
    
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200: #product updated successfully
            from django.core.cache import cache
            product = response.data # Get the updated product data
            cache.set(
                f"product_data_{product['id']}",
                {
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"],
                },
            ) # Cache the updated product data
        return response


class ProductStats(GenericAPIView):
    lookup_field = 'id'
    serializer_class = ProductStatSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None, id=None):
        obj = self.get_object()
        serializer = ProductStatSerializer(
            {
                'stats':{
                    '2019-01-01': [5, 10, 15],
                    '2019-01-02': [10, 20, 30],
                }
            }
        )
        return Response(serializer.data)
