import os
import django
import sys

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from django.contrib.auth.models import User
from django.db import IntegrityError

def create_test_users():
    # Create regular users
    regular_users = []
    for i in range(1, 6):
        username = f"user{i}"
        email = f"user{i}@example.com"
        password = f"testpass{i}"
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=f"User",
                last_name=f"Number {i}"
            )
            regular_users.append((username, password))
            print(f"Created regular user: {username} with password: {password}")
        except IntegrityError:
            print(f"User {username} already exists.")
    
    # Create admin user
    try:
        admin_username = 'admin'
        admin_password = 'adminpass123'
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email='admin@example.com',
            password=admin_password,
            first_name='Admin',
            last_name='User'
        )
        print(f"Created admin user: {admin_username} with password: {admin_password}")
    except IntegrityError:
        print(f"Admin user already exists.")
    
    # Print summary
    print("\n--- TEST USERS CREATED ---")
    print("REGULAR USERS:")
    for username, password in regular_users:
        print(f"Username: {username} | Password: {password}")
    
    print("\nADMIN USER:")
    print(f"Username: admin | Password: adminpass123")
    print("\nUse these credentials to log into the system for testing.")

if __name__ == "__main__":
    create_test_users()