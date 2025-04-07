#!/usr/bin/env python
"""
Replit deployment helper script for My Cutipie Kids Factory Outlet.
This script performs the necessary setup for deploying on Replit.
"""

import os
import sys
import django
import subprocess
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings_replit')
django.setup()

def main():
    """Main deployment function."""
    print("Starting Replit deployment process...")
    
    # Collect static files
    print("Collecting static files...")
    call_command('collectstatic', interactive=False)
    
    # Apply migrations
    print("Applying database migrations...")
    call_command('migrate')
    
    # Check if test users exist, create them if not
    from django.contrib.auth.models import User
    from django.db.models import Q
    
    # Check if admin user exists
    admin_exists = User.objects.filter(
        Q(username='admin') | Q(email='anilsherikar207@gmail.com')
    ).exists()
    
    if not admin_exists:
        print("Creating admin user...")
        User.objects.create_superuser('admin', 'admin@example.com', 'adminpass123')
        User.objects.create_superuser('anil_admin', 'anilsherikar207@gmail.com', 'adminpass123')
    
    # Check if test users exist
    for i in range(1, 6):
        username = f'user{i}'
        if not User.objects.filter(username=username).exists():
            print(f"Creating test user: {username}")
            User.objects.create_user(username, f'user{i}@example.com', f'testpass{i}')
    
    # Create sample data if environment variable is set
    if os.environ.get('CREATE_SAMPLE_DATA') == 'True':
        print("Creating sample data...")
        try:
            # Import and run sample data creation function
            from create_sample_data import create_sample_data
            create_sample_data()
            print("Sample data created successfully.")
        except Exception as e:
            print(f"Error creating sample data: {e}")
    
    # Create country codes
    try:
        from create_country_codes import create_country_codes
        create_country_codes()
        print("Country codes created successfully.")
    except Exception as e:
        print(f"Error creating country codes: {e}")
    
    print("Deployment setup complete!")
    
    # Start the server
    print("Starting server...")
    subprocess.run([
        "python", "manage.py", "runserver", "0.0.0.0:5000", 
        "--settings=clothing_store.settings_replit"
    ])

if __name__ == "__main__":
    main()