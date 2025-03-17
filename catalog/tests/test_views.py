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

    # Add negative test cases to improve coverage
    def test_create_category_invalid_data(self):
        url = reverse('catalog:category-list-create')
        data = {'name': ''}  # Invalid data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product_invalid_data(self):
        url = reverse('catalog:product-detail', args=[self.product.id])
        data = {'regular_price': -10}  # Invalid price
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_inventory_invalid_quantity(self):
        url = reverse('catalog:inventory-update', args=[self.product.id])
        data = {'quantity': -1}  # Invalid quantity
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_get_category_list(self):
        url = reverse('catalog:category-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_category_detail(self):
        url = reverse('catalog:category-detail', args=[self.category.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

    def test_update_category(self):
        url = reverse('catalog:category-detail', args=[self.category.id])
        data = {'name': 'Updated Category', 'slug': 'updated-category'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')

    def test_delete_category(self):
        url = reverse('catalog:category-detail', args=[self.category.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

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

    def test_get_product_list(self):
        url = reverse('catalog:product-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_product_detail(self):
        url = reverse('catalog:product-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Product')

    def test_update_product(self):
        url = reverse('catalog:product-detail', args=[self.product.id])
        data = {'name': 'Updated Product'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Product')

    def test_get_inventory(self):
        url = reverse('catalog:inventory-detail', args=[self.product.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 10)

    def test_update_inventory(self):
        url = reverse('catalog:inventory-update', args=[self.product.id])
        data = {'quantity': 20}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 20)
