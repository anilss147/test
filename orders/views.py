from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem
from .forms import CheckoutForm
from cart.cart import Cart
from products.models import Product


@login_required
def checkout_view(request):
    """
    View to handle the checkout process.
    """
    cart = Cart(request)
    
    # Redirect to cart if the cart is empty
    if len(cart) == 0:
        messages.error(request, "Your cart is empty. Please add some products first.")
        return redirect('cart:view')
    
    # Check if products are still available and in stock
    for item in cart:
        product = item['product']
        if not product.available:
            messages.error(request, f"{product.name} is no longer available. It has been removed from your cart.")
            cart.remove(product)
            return redirect('cart:view')
        if product.stock < item['quantity']:
            messages.error(request, f"Only {product.stock} units of {product.name} are available. Please update your cart.")
            return redirect('cart:view')
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # Create order
                    order = Order.objects.create(
                        user=request.user,
                        first_name=form.cleaned_data['first_name'],
                        last_name=form.cleaned_data['last_name'],
                        email=form.cleaned_data['email'],
                        phone=form.cleaned_data['phone'],
                        address=form.cleaned_data['address'],
                        address2=form.cleaned_data['address2'],
                        city=form.cleaned_data['city'],
                        state=form.cleaned_data['state'],
                        postal_code=form.cleaned_data['postal_code'],
                        country=form.cleaned_data['country'],
                        payment_method=form.cleaned_data['payment_method'],
                        subtotal_price=cart.get_subtotal_price(),
                        shipping_price=cart.get_shipping_cost(),
                        discount=cart.get_discount(),
                        total_price=cart.get_final_price(),
                    )
                    
                    # Create order items
                    for item in cart:
                        product = item['product']
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            price=item['price'],
                            quantity=item['quantity'],
                            size=item.get('size'),
                            color=item.get('color')
                        )
                        
                        # Update product stock
                        product.stock -= item['quantity']
                        product.save()
                    
                    # Process payment (simplified for this implementation)
                    # In a real-world scenario, you would integrate with a payment processor
                    order.paid = True
                    order.status = 'processing'
                    order.transaction_id = f"TXID-{timezone.now().strftime('%Y%m%d%H%M%S')}"
                    order.save()
                    
                    # Clear the cart
                    cart.clear()
                    
                    # Add loyalty points to user's profile (10 points per $1 spent)
                    request.user.profile.loyalty_points += int(order.total_price * 10)
                    request.user.profile.save()
                    
                    # Redirect to order success page
                    return redirect('orders:success', order_id=order.id)
            
            except Exception as e:
                # Handle any exceptions during order processing
                messages.error(request, f"An error occurred during checkout: {str(e)}")
                return redirect('orders:checkout')
    else:
        # Pre-fill the form with user information if available
        initial_data = {}
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
        
        # Add profile information if available
        profile = request.user.profile
        if profile.phone_number:
            initial_data['phone'] = profile.phone_number
        if profile.address:
            initial_data['address'] = profile.address
        if profile.city:
            initial_data['city'] = profile.city
        if profile.state:
            initial_data['state'] = profile.state
        if profile.postal_code:
            initial_data['postal_code'] = profile.postal_code
        if profile.country:
            initial_data['country'] = profile.country
        
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart,
    }
    
    return render(request, 'orders/checkout.html', context)


@login_required
def order_success_view(request, order_id):
    """
    View to display order success page.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_success.html', context)


@login_required
def order_history_view(request):
    """
    View to display user's order history.
    """
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    
    return render(request, 'orders/order_history.html', context)


@login_required
def order_detail_view(request, order_id):
    """
    View to display order details.
    """
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
    }
    
    return render(request, 'orders/order_detail.html', context)
