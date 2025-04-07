from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q
import re

class EmailOrPhoneModelBackend(ModelBackend):
    """
    Authentication backend that allows users to login with either
    email address or phone number (with country code) along with username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on email address OR phone number OR username.
        """
        if not username or not password:
            return None
            
        # Check if the input looks like a phone number with country code
        # Pattern like +1234567890 or 00123456789
        phone_with_code_pattern = r'^(\+|00)(\d+)$'
        phone_match = re.match(phone_with_code_pattern, username)
        
        try:
            # Try to find a user first by exact match
            user_query = Q(username=username) | Q(email=username) 
            
            # If it looks like a phone with country code
            if phone_match:
                # Extract just the numbers for comparison
                phone_digits = re.sub(r'[^0-9]', '', username)
                
                # Add phone-specific query conditions
                user_query = user_query | Q(profile__phone_number=username)
                
                # Try to also match by getting the full phone from profile
                # This checks for users where country code and phone are stored separately
                for user in User.objects.filter(profile__phone_number__isnull=False):
                    if user.profile.get_full_phone_number() and re.sub(r'[^0-9]', '', user.profile.get_full_phone_number()) == phone_digits:
                        # Check password
                        if user.check_password(password):
                            return user
            
            # Find users matching the basic criteria
            user = User.objects.get(user_query)
            
            # Check the password
            if user.check_password(password):
                return user
                
        except User.DoesNotExist:
            # No user was found matching the credentials
            return None
            
        # Incorrect password
        return None