from rest_framework import status
from django.urls import reverse
from catalog.models import Category
from .test_base import BaseAPITestCase

class CatalogAPITests(BaseAPITestCase):
    def test_create_category(self):
        # Create initial category
        initial_response = self.create_category()
        self.assertEqual(initial_response.status_code, status.HTTP_201_CREATED)

        # Create second category with different data
        url = reverse('catalog:category-list-create')
        data = {
            'name': 'Second Category',
            'description': 'Second Description',
            'slug': 'second-category'
        }

        second_response = self.client.post(url, data, format='json')
        self.assertEqual(second_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
