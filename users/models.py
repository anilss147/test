from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class CountryCode(models.Model):
    """
    Model to store country codes for phone numbers.
    """
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    flag_emoji = models.CharField(max_length=10, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        ordering = ['name']


class Profile(models.Model):
    """
    Extended user profile model to store additional user information.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country_code = models.ForeignKey(CountryCode, on_delete=models.SET_NULL, null=True, blank=True)
    is_phone_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    preferred_login_method = models.CharField(
        max_length=10,
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
        ],
        default='email'
    )
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    
    # Loyalty program fields
    loyalty_points = models.PositiveIntegerField(default=0)
    
    # Preferences and tracking
    subscribed_to_newsletter = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def get_full_phone_number(self):
        """
        Return the full phone number with country code.
        """
        if self.phone_number and self.country_code:
            return f"{self.country_code.code} {self.phone_number}"
        return self.phone_number


# Create Profile automatically when a new user is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
