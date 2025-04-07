from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Profile, CountryCode


class CustomUserCreationForm(UserCreationForm):
    """
    Extends the built-in UserCreationForm to add email field as required.
    Also adds custom styling for all form fields.
    """
    email = forms.EmailField(
        max_length=254,
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Email'
        })
    )
    
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Phone Number'
        })
    )
    
    country_code = forms.ModelChoiceField(
        queryset=CountryCode.objects.all(),
        required=False,
        empty_label="Select Country Code",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    preferred_login_method = forms.ChoiceField(
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        initial='email'
    )
    
    first_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'First Name'
        })
    )
    
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Last Name'
        })
    )
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username'
        })
    )
    
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password'
        })
    )
    
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Confirm Password'
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        preferred_login_method = cleaned_data.get('preferred_login_method')
        phone_number = cleaned_data.get('phone_number')
        country_code = cleaned_data.get('country_code')
        
        if preferred_login_method == 'phone' and (not phone_number or not country_code):
            raise ValidationError(
                _("Phone number and country code are required when phone login method is selected.")
            )
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        
        if commit:
            user.save()
            # Update profile fields
            user.profile.phone_number = self.cleaned_data.get('phone_number')
            user.profile.country_code = self.cleaned_data.get('country_code')
            user.profile.preferred_login_method = self.cleaned_data.get('preferred_login_method')
            user.profile.save()
        
        return user


class LoginMethodForm(forms.Form):
    """
    Form to select the login method (email or phone)
    """
    login_method = forms.ChoiceField(
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        initial='email'
    )


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with styled widgets that supports both username/email and phone login.
    """
    # Override username field to accept email, username or phone
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Username, Email, or Phone Number'
        })
    )
    
    # Add country code field for phone login
    country_code = forms.ModelChoiceField(
        queryset=CountryCode.objects.all(),
        required=False,
        empty_label="Select Country Code",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'id': 'id_country_code'
        })
    )
    
    # Add a field to specify login method
    login_method = forms.ChoiceField(
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300'
        }),
        initial='email'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.
    """
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }


class ProfileDetailForm(forms.ModelForm):
    """
    Form for updating profile details.
    """
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
            'placeholder': 'Phone Number'
        })
    )
    
    country_code = forms.ModelChoiceField(
        queryset=CountryCode.objects.all(),
        required=False,
        empty_label="Select Country Code",
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
        })
    )
    
    preferred_login_method = forms.ChoiceField(
        choices=[
            ('email', _('Email')),
            ('phone', _('Phone')),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300'
        })
    )
    
    class Meta:
        model = Profile
        fields = ('phone_number', 'country_code', 'preferred_login_method', 'address', 'city', 'state', 'postal_code', 'country')
        widgets = {
            'address': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'state': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'postal_code': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500'
            }),
        }
