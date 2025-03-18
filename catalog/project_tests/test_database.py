from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError
from catalog.models import Category, Product, Inventory

class DatabaseTest(TestCase):
    def test_database_connection(self):
        db_conn = connections['default']
        try:
            db_conn.cursor()
            self.assertIsNotNone(db_conn)
        except OperationalError:
            self.fail("Database connection failed")

    def test_model_relationships(self):
        # Test Category creation
        category = Category.objects.create(
            name="Test Category",
            slug="test-category"
        )
        self.assertIsNotNone(category.id)

        # Test Product creation with Category
        product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            sku="TEST123",
            regular_price=99.99,
            category=category
        )
        self.assertIsNotNone(product.id)
        self.assertEqual(product.category, category)

        # Test Inventory creation with Product
        inventory = Inventory.objects.create(
            product=product,
            quantity=10
        )
        self.assertIsNotNone(inventory.id)
        self.assertEqual(inventory.product, product)
