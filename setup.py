"""
Quick setup script to initialize the News Aggregator project.
Run this after installing dependencies to set up the database and fetch initial news.
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newsaggregator.settings')
django.setup()

from django.core.management import execute_from_command_line

if __name__ == '__main__':
    print("Setting up News Aggregator...")
    print("1. Making migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    print("2. Running migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    print("3. Fetching initial news data...")
    execute_from_command_line(['manage.py', 'fetch_news'])
    
    print("\n✅ Setup complete!")
    print("Run 'python manage.py runserver' to start the development server.")

