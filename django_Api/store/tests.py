import os.path
from django.conf import settings

from rest_framework.test import APITestCase
from decimal import Decimal

from store.models import Product

class ProductCreateTestCase(APITestCase):
    def test_create_product(self):
        initial_product_count = Product.objects.count()
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product',
            'price': '123.45',
        }
        response = self.client.post('/api/v1/products/new', product_attrs)
        if response.status_code != 201:
            print(response.data)
        self.assertEqual(
            Product.objects.count(),
            initial_product_count + 1,
        )
        for attr, expected_value in product_attrs.items():
            self.assertEqual(response.data[attr], expected_value)
        self.assertEqual(response.data['is_on_sale'], False)
        self.assertEqual(
            response.data['current_price'],
            float(product_attrs['price']),
        )


class ProductDestroyTestCase(APITestCase):
    def create_product(self):
        product_attrs = {
            'name': 'New Product',
            'description': 'Awesome product',
            'price': Decimal('123.45'),
        }
        response = self.client.post('/api/v1/products/new', product_attrs)
        self.assertEqual(response.status_code, 201)
        return response.data['id']

    def test_delete_product(self):
        product_id = self.create_product()
        initial_product_count = Product.objects.count()

        delete_response = self.client.delete(f'/api/v1/products/{product_id}')
        self.assertEqual(delete_response.status_code, 204)
        self.assertEqual(Product.objects.count(), initial_product_count - 1)
        self.assertRaises(Product.DoesNotExist, Product.objects.get, id=product_id)

class ProductListTestCase(APITestCase):
    def test_list_products(self):
        products_count = Product.objects.count()
        response = self.client.get('/api/v1/products')
        self.assertIsNone(response.data['next'])
        self.assertIsNone(response.data['previous'])
        self.assertEqual(response.data['count'], products_count)
        self.assertEqual(len(response.data['results']), products_count)



class ProductUpdateTestCase(APITestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name='Old Product',
            description='Old description',
            price=Decimal('100.00'),
        )

    def test_update_product(self):
        url = f'/api/v1/products/{self.product.id}'
        response = self.client.patch(
            url,
            {
                'name': 'New Product',
                'description': 'Awesome product',
                'price': '123.45',
            },
            format='json',
        )
        print("Status code:", response.status_code)
        print("Content:", response.content)

        self.assertEqual(response.status_code, 200)
        updated = Product.objects.get(id=self.product.id)
        self.assertEqual(updated.name, 'New Product')
    
    def test_upload_product_photo(self):
        product = Product.objects.first()
        original_photo = product.photo
        photo_path = os.path.join(settings.MEDIA_ROOT, 'products', 'vitamin-iron.jpg')
        with open(photo_path, 'rb') as photo_data:
            response = self.client.patch('/api/v1/products/{}'.format(product.id), {
                'photo': photo_data,
            }, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.data['photo'], original_photo)
        try:
            updated = Product.objects.get(id=product.id)
            expected_photo = os.path.join(settings.MEDIA_ROOT, 'products', 'vitamin-iron')
            self.assertTrue(updated.photo.path.startswith(expected_photo))
        finally:
            os.remove(updated.photo.path)
