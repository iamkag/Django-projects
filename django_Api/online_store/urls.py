from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import store.views
import store.api_views

urlpatterns = [
    path('api/v1/products', store.api_views.ProductList.as_view()),   # API JSON list of products
    path('api/v1/products/new', store.api_views.ProductCreate.as_view()), # API endpoint to create a new product
    #path('api/v1/products/<int:id>/destroy', store.api_views.ProductDestroy.as_view()), # API endpoint to get, update or delete a product
    path('api/v1/products/<int:id>', store.api_views.ProductRetrieveUpdateDestroy.as_view()), # API endpoint to get, update or delete a product
    path('api/v1/products/<int:id>/stats', store.api_views.ProductStats.as_view()), # API endpoint to get product stats
    
    path('admin/', admin.site.urls),
    path('products/<int:id>/', store.views.show, name='show-product'), # Single product detail page
    path('cart/', store.views.cart, name='shopping-cart'),             # Shopping cart page
    path('', store.views.index, name='list-products'),                 # Product listing page    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)     # Serve uploaded media in dev mode
