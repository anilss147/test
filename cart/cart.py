from decimal import Decimal
from django.conf import settings
from products.models import Product


class Cart:
    """
    A class to manage the shopping cart session data.
    """
    
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
    
    def add(self, product, quantity=1, override_quantity=False, size=None, color=None):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.discount_price if product.discount_price else product.price),
                'size': size,
                'color': color
            }
        
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        
        # Update size and color if provided
        if size:
            self.cart[product_id]['size'] = size
        if color:
            self.cart[product_id]['color'] = color
            
        self.save()
    
    def save(self):
        """
        Mark the session as modified to ensure it gets saved.
        """
        self.session.modified = True
    
    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    
    def update_quantity(self, product, quantity):
        """
        Update quantity for a specific product.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()
    
    def update_size_color(self, product, size, color):
        """
        Update size and color for a specific product.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['size'] = size
            self.cart[product_id]['color'] = color
            self.save()
    
    def clear(self):
        """
        Remove cart from session.
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
    
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def get_total_price(self):
        """
        Calculate the total cost of all items in the cart.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())
    
    def get_subtotal_price(self):
        """
        Calculate the subtotal (before any discounts)
        """
        return self.get_total_price()
    
    def get_discount(self):
        """
        Calculate any discount to be applied to the cart.
        This is a placeholder for future discount functionality.
        """
        return Decimal('0')
    
    def get_shipping_cost(self):
        """
        Calculate shipping cost based on cart total.
        Free shipping over $50.
        """
        if self.get_subtotal_price() >= Decimal('50.00'):
            return Decimal('0')
        return Decimal('5.99')
    
    def get_final_price(self):
        """
        Calculate the final price including shipping and discounts.
        """
        return self.get_subtotal_price() - self.get_discount() + self.get_shipping_cost()
