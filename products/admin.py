from django.contrib import admin
from django.utils.html import mark_safe
from .models import (
    Category, Product, ProductImage, 
    ProductReview, ProductVariant, 
    ProductLabel, ProductLabelRelation
)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    
    
class ProductLabelInline(admin.TabularInline):
    model = ProductLabelRelation
    extra = 1
    autocomplete_fields = ['label']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'discount_price', 'stock', 'available', 'is_featured', 'gender', 'display_labels')
    list_filter = ('available', 'is_featured', 'is_new', 'gender', 'category', 'product_labels__label')
    list_editable = ('price', 'discount_price', 'stock', 'available', 'is_featured')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline, ProductLabelInline]
    
    def display_labels(self, obj):
        """Display all labels as colored badges"""
        labels = obj.get_labels()
        if not labels:
            return '-'
        
        html = ''
        for label in labels:
            html += f'<span style="background-color: {label.background_color}; color: {label.color}; padding: 3px 6px; border-radius: 3px; margin-right: 5px; font-size: 0.8em;">{label.display_name}</span>'
        
        return mark_safe(html)
    
    display_labels.short_description = 'Labels'


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'review')


@admin.register(ProductLabel)
class ProductLabelAdmin(admin.ModelAdmin):
    list_display = ('display_name', 'name', 'color_tag', 'priority', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    list_editable = ('priority', 'is_active')
    search_fields = ('name', 'display_name', 'description')
    ordering = ('-priority', 'display_name')
    
    def get_fields(self, request, obj=None):
        fields = ['name', 'display_name', 'description', 'color', 'background_color', 'priority', 'is_active']
        if obj:  # If editing an existing object
            fields.append('color_tag')
        return fields
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return ['color_tag']
        return []


@admin.register(ProductLabelRelation)
class ProductLabelRelationAdmin(admin.ModelAdmin):
    list_display = ('product', 'label', 'added_at')
    list_filter = ('label', 'added_at')
    search_fields = ('product__name', 'label__name', 'label__display_name')
    autocomplete_fields = ['product', 'label']
