from django.contrib import admin
from .models import Order, OrderItem, Payment


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0


class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'email', 'total_price', 'status', 'paid', 'created_at']
    list_filter = ['status', 'paid', 'created_at']
    search_fields = ['id', 'first_name', 'last_name', 'email']
    readonly_fields = ['id', 'created_at', 'updated_at']
    inlines = [OrderItemInline, PaymentInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'user', 'status', 'paid', 'created_at', 'updated_at')
        }),
        ('Customer Information', {
            'fields': ('first_name', 'last_name', 'email', 'phone')
        }),
        ('Shipping Address', {
            'fields': ('address', 'address2', 'city', 'state', 'postal_code', 'country')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'transaction_id', 'subtotal_price', 'shipping_price', 'discount', 'total_price')
        }),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'amount', 'status', 'payment_method', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['id', 'order__id', 'transaction_id']
    readonly_fields = ['id', 'created_at']
