from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from catalog.models import Category, Product, Inventory

class CatalogAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category",
            description="Test Description",
            slug="test-category"
        )

        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST123",
            regular_price=99.99,
            category=self.category
        )

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

    def test_get_categories(self):
        url = reverse('catalog:category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)