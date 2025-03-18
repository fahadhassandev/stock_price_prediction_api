from rest_framework import status
from django.urls import reverse
from .test_base import BaseAPITestCase

class CatalogViewsTest(BaseAPITestCase):
    def test_category_crud(self):
        # Create
        response = self.create_category()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        category_id = response.data['id']

        # Read
        url = reverse('catalog:category-detail', args=[category_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')

        # Update
        update_data = {'name': 'Updated Category'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Category')

        # Delete
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_crud(self):
        # Create category first
        category_response = self.create_category()
        category_id = category_response.data['id']

        # Create product
        response = self.create_product(category_id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        product_id = response.data['id']

        # Read product
        url = reverse('catalog:product-detail', args=[product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update product
        update_data = {'name': 'Updated Product'}
        response = self.client.patch(url, update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Delete product
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_operations(self):
        # Test invalid category creation
        url = reverse('catalog:category-list-create')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid product creation
        url = reverse('catalog:product-list-create')
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test non-existent category
        url = reverse('catalog:category-detail', args=[999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
