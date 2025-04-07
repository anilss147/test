from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum, Avg
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

from products.models import Product, Category
from orders.models import Order, OrderItem
from users.models import Profile


def is_staff(user):
    """Check if a user is staff or has specific admin email."""
    return user.is_staff or user.email == 'anilsherikar207@gmail.com'


@login_required
@user_passes_test(is_staff)
def dashboard_home(request):
    """
    Main dashboard view for the admin panel.
    Shows overview statistics and recent activity.
    """
    # Get stats for the last 30 days
    thirty_days_ago = timezone.now() - timedelta(days=30)
    
    # Recent orders
    recent_orders = Order.objects.order_by('-created_at')[:5]
    
    # Sales statistics
    total_sales = Order.objects.filter(created_at__gte=thirty_days_ago).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    total_orders = Order.objects.filter(created_at__gte=thirty_days_ago).count()
    
    # Product statistics
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(stock__lt=10).count()
    
    # User statistics
    total_users = User.objects.count()
    new_users = User.objects.filter(date_joined__gte=thirty_days_ago).count()
    
    # Popular products (most ordered)
    popular_products = Product.objects.annotate(
        order_count=Count('order_items')
    ).order_by('-order_count')[:5]
    
    context = {
        'recent_orders': recent_orders,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'total_users': total_users,
        'new_users': new_users,
        'popular_products': popular_products,
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
@user_passes_test(is_staff)
def dashboard_products(request):
    """
    View to manage products in the admin panel.
    """
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    context = {
        'products': products,
        'categories': categories,
    }
    
    return render(request, 'dashboard/products.html', context)


@login_required
@user_passes_test(is_staff)
def dashboard_orders(request):
    """
    View to manage orders in the admin panel.
    """
    orders = Order.objects.all().order_by('-created_at')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status:
        orders = orders.filter(status=status)
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status,
    }
    
    return render(request, 'dashboard/orders.html', context)


@login_required
@user_passes_test(is_staff)
def dashboard_customers(request):
    """
    View to manage customers in the admin panel.
    """
    users = User.objects.all().order_by('-date_joined')
    
    # Add order count and total spent for each user
    for user in users:
        user.order_count = Order.objects.filter(user=user).count()
        user.total_spent = Order.objects.filter(user=user).aggregate(
            total=Sum('total_price')
        )['total'] or 0
    
    context = {
        'users': users,
    }
    
    return render(request, 'dashboard/customers.html', context)


@login_required
@user_passes_test(is_staff)
def dashboard_analytics(request):
    """
    View for analytics and reporting in the admin panel.
    """
    # Sales by period
    this_month = timezone.now().replace(day=1, hour=0, minute=0, second=0)
    last_month = (this_month - timedelta(days=1)).replace(day=1)
    
    # This month's sales
    this_month_sales = Order.objects.filter(created_at__gte=this_month).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Last month's sales
    last_month_sales = Order.objects.filter(
        created_at__gte=last_month,
        created_at__lt=this_month
    ).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    
    # Sales by gender category
    sales_by_gender = []
    for gender_code, gender_name in Product.GENDER_CHOICES:
        sales = OrderItem.objects.filter(
            product__gender=gender_code
        ).aggregate(
            total=Sum('price')
        )['total'] or 0
        sales_by_gender.append({
            'name': gender_name,
            'value': sales
        })
    
    # Top selling products
    top_products = Product.objects.annotate(
        sold=Sum('order_items__quantity')
    ).order_by('-sold')[:10]
    
    # Order status distribution
    status_distribution = []
    for status_code, status_name in Order.STATUS_CHOICES:
        count = Order.objects.filter(status=status_code).count()
        status_distribution.append({
            'name': status_name,
            'value': count
        })
    
    context = {
        'this_month_sales': this_month_sales,
        'last_month_sales': last_month_sales,
        'sales_by_gender': sales_by_gender,
        'top_products': top_products,
        'status_distribution': status_distribution,
    }
    
    return render(request, 'dashboard/analytics.html', context)
