from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Category, Product, Inventory

class CatalogAPITests(APITestCase):
    def setUp(self):
        # Create test category
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            slug="test-category"
        )

        # Create test product
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST123",
            regular_price=99.99,
            category=self.category
        )

        # Create test inventory
        self.inventory = Inventory.objects.create(
            product=self.product,
            quantity=10,
            low_stock_threshold=5
        )

    def test_create_category(self):
        url = reverse('catalog:category-list-create')
        data = {
            'name': 'New Category',
            'description': 'New Description',
            'slug': 'new-category'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)

    def test_create_product(self):
        url = reverse('catalog:product-list-create')
        data = {
            'name': 'New Product',
            'description': 'New Description',
            'sku': 'NEW123',
            'regular_price': '199.99',
            'category': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 2)