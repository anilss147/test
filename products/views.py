from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product, Category, ProductReview
from wishlist.models import WishlistItem


def product_list(request):
    """
    View to display all products with filtering options.
    """
    products = Product.objects.filter(available=True)
    categories = Category.objects.filter(is_active=True)
    
    # Filter products based on query parameters
    category_id = request.GET.get('category')
    gender = request.GET.get('gender')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort', 'newest')
    on_sale = request.GET.get('on_sale')
    search_query = request.GET.get('q')
    
    if category_id:
        products = products.filter(category_id=category_id)
    
    if gender:
        products = products.filter(gender=gender)
    
    if min_price:
        products = products.filter(price__gte=float(min_price))
    
    if max_price:
        products = products.filter(price__lte=float(max_price))
    
    if on_sale:
        products = products.filter(discount_price__isnull=False)
    
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )
    
    # Sort products
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    elif sort == 'popular':
        products = products.order_by('-reviews__rating')
    
    # Pagination
    paginator = Paginator(products, 12)  # Show 12 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_id,
        'selected_gender': gender,
        'selected_min_price': min_price,
        'selected_max_price': max_price,
        'selected_sort': sort,
        'search_query': search_query,
    }
    
    return render(request, 'products/product_list.html', context)


def product_detail(request, product_id):
    """
    View to display detailed information about a product.
    """
    product = get_object_or_404(Product, id=product_id, available=True)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    is_in_wishlist = False
    
    # Check if product is in user's wishlist
    if request.user.is_authenticated:
        is_in_wishlist = WishlistItem.objects.filter(user=request.user, product=product).exists()
    
    # Handle product review form
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')
        
        if rating and review_text:
            ProductReview.objects.update_or_create(
                product=product,
                user=request.user,
                defaults={
                    'rating': rating,
                    'review': review_text
                }
            )
            messages.success(request, "Thank you for your review!")
            return redirect('products:detail', product_id=product.id)
    
    context = {
        'product': product,
        'related_products': related_products,
        'is_in_wishlist': is_in_wishlist,
    }
    
    return render(request, 'products/product_detail.html', context)


def category_list(request, gender_or_category):
    """
    View to display products by category or gender.
    """
    # Check if the parameter is a gender
    if gender_or_category in ['men', 'women', 'kids']:
        products = Product.objects.filter(gender=gender_or_category, available=True)
        category_name = gender_or_category.capitalize()
    else:
        # Treat it as a category slug
        category = get_object_or_404(Category, slug=gender_or_category)
        products = Product.objects.filter(category=category, available=True)
        category_name = category.name
    
    context = {
        'products': products,
        'category_name': category_name,
    }
    
    return render(request, 'products/category_list.html', context)


def search_products(request):
    """
    View to handle product search.
    """
    query = request.GET.get('q', '')
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(available=True)
    else:
        products = Product.objects.none()
    
    context = {
        'products': products,
        'search_query': query,
    }
    
    return render(request, 'products/search_results.html', context)
