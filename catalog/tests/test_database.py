from django.test import TestCase
from django.db import connections
from django.db.utils import OperationalError

class DatabaseConnectionTest(TestCase):
    def test_database_connection(self):
        db_conn = connections['default']
        try:
            c = db_conn.cursor()
            self.assertTrue(True)  # Connection successful
        except OperationalError:
            self.fail("Database connection failed")