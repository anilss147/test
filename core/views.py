from django.shortcuts import render
from products.models import Product, Category

def home(request):
    """Home page view that prioritizes kids products."""
    # Get kids products first
    kids_featured_products = Product.objects.filter(
        is_featured=True, 
        category__name__icontains='kid'
    )[:8]
    
    # If not enough kids featured products, add other featured products
    if kids_featured_products.count() < 8:
        other_featured = Product.objects.filter(
            is_featured=True
        ).exclude(
            id__in=[p.id for p in kids_featured_products]
        )[:8-kids_featured_products.count()]
        
        # Combine querysets
        featured_products = list(kids_featured_products) + list(other_featured)
    else:
        featured_products = kids_featured_products
        
    # Prioritize kids new arrivals
    kids_new_arrivals = Product.objects.filter(
        category__name__icontains='kid'
    ).order_by('-created_at')[:8]
    
    # If not enough kids new arrivals, add other new products
    if kids_new_arrivals.count() < 8:
        other_new = Product.objects.order_by(
            '-created_at'
        ).exclude(
            id__in=[p.id for p in kids_new_arrivals]
        )[:8-kids_new_arrivals.count()]
        
        new_arrivals = list(kids_new_arrivals) + list(other_new)
    else:
        new_arrivals = kids_new_arrivals
    
    categories = Category.objects.filter(parent=None)
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def about(request):
    """About page view."""
    return render(request, 'core/about.html')

def contact(request):
    """Contact page view."""
    return render(request, 'core/contact.html')
