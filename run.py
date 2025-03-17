import os
import sys
import django
from django.core.management import execute_from_command_line

def run_tests():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    django.setup()
    execute_from_command_line(['manage.py', 'test'])

if __name__ == '__main__':
    run_tests()