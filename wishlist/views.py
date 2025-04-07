from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import WishlistItem
from products.models import Product


@login_required
def wishlist_view(request):
    """
    View to display the user's wishlist.
    """
    wishlist_items = WishlistItem.objects.filter(user=request.user)
    
    context = {
        'wishlist_items': wishlist_items,
    }
    
    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """
    Add a product to the user's wishlist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Check if the product is already in the wishlist
    if WishlistItem.objects.filter(user=request.user, product=product).exists():
        messages.info(request, f"{product.name} is already in your wishlist.")
    else:
        # Add the product to the wishlist
        WishlistItem.objects.create(user=request.user, product=product)
        messages.success(request, f"{product.name} has been added to your wishlist.")
    
    # Handle AJAX requests
    if request.is_ajax():
        return JsonResponse({'success': True})
    
    # Redirect to the referring page or product detail page
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('products:detail', product_id=product.id)


@login_required
def remove_from_wishlist(request, product_id):
    """
    Remove a product from the user's wishlist.
    """
    product = get_object_or_404(Product, id=product_id)
    
    # Try to get and delete the wishlist item
    try:
        wishlist_item = WishlistItem.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, f"{product.name} has been removed from your wishlist.")
    except WishlistItem.DoesNotExist:
        messages.error(request, f"{product.name} is not in your wishlist.")
    
    # Handle AJAX requests
    if request.is_ajax():
        return JsonResponse({'success': True})
    
    # Redirect to the referring page or wishlist page
    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('wishlist:view')


@login_required
def clear_wishlist(request):
    """
    Clear all items from the user's wishlist.
    """
    WishlistItem.objects.filter(user=request.user).delete()
    messages.success(request, "Your wishlist has been cleared.")
    
    return redirect('wishlist:view')
