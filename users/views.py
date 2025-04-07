from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm,
    UserProfileForm, ProfileDetailForm, LoginMethodForm
)
from .models import CountryCode, Profile
from orders.models import Order


def register(request):
    """
    User registration view.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Get username and password from form data
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            # Authenticate and login the user
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, "Registration successful! Welcome to StyleShop.")
            return redirect('core:home')
        else:
            messages.error(request, "There was an error with your registration. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    # Ensure all country codes are available
    if CountryCode.objects.count() == 0:
        from .management.commands.create_country_codes import Command
        Command().handle()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    User login view.
    """
    if request.user.is_authenticated:
        return redirect('core:home')
    
    # Initialize empty forms
    auth_form = CustomAuthenticationForm()
    method_form = LoginMethodForm()
    
    if request.method == 'POST':
        # Check if the method selection form was submitted
        if 'login_method' in request.POST:
            method_form = LoginMethodForm(request.POST)
            if method_form.is_valid():
                # Return the same page with the selected method
                method = method_form.cleaned_data.get('login_method')
                auth_form = CustomAuthenticationForm(initial={'login_method': method})
                return render(request, 'users/login.html', {
                    'form': auth_form,
                    'method_form': method_form,
                    'selected_method': method
                })
                
        # Handle the actual login form submission
        auth_form = CustomAuthenticationForm(data=request.POST)
        if auth_form.is_valid():
            username = auth_form.cleaned_data.get('username')
            password = auth_form.cleaned_data.get('password')
            login_method = auth_form.cleaned_data.get('login_method')
            
            # Prepare the actual authentication username based on login method
            auth_username = username
            
            # Get country code if phone login method is selected
            if login_method == 'phone':
                country_code = auth_form.cleaned_data.get('country_code')
                if country_code:
                    # Format username with country code for phone login
                    # Our custom backend will check this format
                    auth_username = f"{country_code.code}{username.strip()}"
                    # Remove any spaces in the phone number
                    auth_username = auth_username.replace(" ", "")
            
            # Authenticate with the appropriate parameters
            user = authenticate(
                request=request,
                username=auth_username,
                password=password
            )
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}!")
                # Redirect to next page if provided, otherwise home
                next_page = request.GET.get('next', 'core:home')
                return redirect(next_page)
            else:
                if login_method == 'email':
                    messages.error(request, "Invalid email or password.")
                elif login_method == 'phone':
                    messages.error(request, "Invalid phone number or password.")
                else:
                    messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Invalid credentials. Please try again.")
    
    # Ensure all country codes are available
    if CountryCode.objects.count() == 0:
        from .management.commands.create_country_codes import Command
        Command().handle()
    
    selected_method = request.POST.get('login_method', 'email')
    return render(request, 'users/login.html', {
        'form': auth_form,
        'method_form': method_form,
        'selected_method': selected_method
    })


@login_required
def profile(request):
    """
    User profile view for displaying and editing profile information.
    """
    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=request.user)
        profile_form = ProfileDetailForm(request.POST, instance=request.user.profile)
        password_form = PasswordChangeForm(request.user, request.POST)
        
        # Check which form was submitted
        if 'update_profile' in request.POST:
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect('users:profile')
            else:
                messages.error(request, "Please correct the errors below.")
        
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                user = password_form.save()
                # Update the session to prevent logging out
                update_session_auth_hash(request, user)
                messages.success(request, "Your password has been changed successfully!")
                return redirect('users:profile')
            else:
                messages.error(request, "Please correct the password errors below.")
    else:
        user_form = UserProfileForm(instance=request.user)
        profile_form = ProfileDetailForm(instance=request.user.profile)
        password_form = PasswordChangeForm(request.user)
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    # Ensure all country codes are available
    if CountryCode.objects.count() == 0:
        from .management.commands.create_country_codes import Command
        Command().handle()
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'users/profile.html', context)
