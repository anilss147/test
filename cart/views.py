from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart


def cart_view(request):
    """
    View to display the shopping cart contents.
    """
    cart = Cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'cart/cart.html', context)


@require_POST
def cart_add(request):
    """
    Add a product to the cart.
    """
    cart = Cart(request)
    product_id = request.POST.get('product_id')
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    size = request.POST.get('size')
    color = request.POST.get('color')
    
    # Get override from request or default to False
    override_quantity = request.POST.get('override', False) == 'True'
    
    # Check if product is available and in stock
    if not product.available:
        messages.error(request, "This product is currently unavailable.")
        return redirect('products:detail', product_id=product_id)
    
    if product.stock < quantity:
        messages.error(request, f"Sorry, only {product.stock} units of this product are available.")
        return redirect('products:detail', product_id=product_id)
    
    cart.add(
        product=product,
        quantity=quantity,
        override_quantity=override_quantity,
        size=size,
        color=color
    )
    
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('cart:view')


@require_POST
def cart_update(request, product_id):
    """
    Update the quantity or size/color of a product in the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    # Get action from request
    action = request.POST.get('action')
    
    if action == 'update_quantity':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            if product.stock >= quantity:
                cart.update_quantity(product, quantity)
                messages.success(request, "Cart updated successfully.")
            else:
                messages.error(request, f"Sorry, only {product.stock} units of this product are available.")
        else:
            cart.remove(product)
            messages.success(request, f"{product.name} has been removed from your cart.")
    
    elif action == 'update_attributes':
        size = request.POST.get('size')
        color = request.POST.get('color')
        cart.update_size_color(product, size, color)
        messages.success(request, "Product options updated successfully.")
    
    return redirect('cart:view')


def cart_remove(request, product_id):
    """
    Remove a product from the cart.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"{product.name} has been removed from your cart.")
    return redirect('cart:view')
