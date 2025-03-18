from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class BaseAPITestCase(APITestCase):
    def setUp(self):
        self.category_data = {
            'name': 'Test Category',
            'description': 'Test Description',
            'slug': 'test-category'
        }
        self.product_data = {
            'name': 'Test Product',
            'description': 'Test Description',
            'sku': 'TEST123',
            'regular_price': '99.99'
        }

    def create_category(self):
        url = reverse('catalog:category-list-create')
        return self.client.post(url, self.category_data, format='json')

    def create_product(self, category_id):
        url = reverse('catalog:product-list-create')
        self.product_data['category'] = category_id
        return self.client.post(url, self.product_data, format='json')

    def create_inventory(self, product_id):
        url = reverse('catalog:inventory-update', args=[product_id])
        data = {'quantity': 10, 'low_stock_threshold': 5}
        return self.client.post(url, data, format='json')

    def test_get_categories(self):
        # Create test category first
        self.create_category()
        url = reverse('catalog:category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
