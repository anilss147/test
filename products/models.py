from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import mark_safe
import uuid
import os


class Category(models.Model):
    """
    Model for product categories with support for hierarchical structure.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ('name',)
    
    def __str__(self):
        if self.parent:
            return f"{self.parent.name} - {self.name}"
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Model for products with inventory tracking.
    """
    GENDER_CHOICES = (
        ('men', 'Men'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('unisex', 'Unisex'),
    )
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('products:detail', args=[str(self.id)])
    
    @property
    def rating(self):
        """Calculate average rating from all reviews."""
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0
    
    @property
    def is_on_sale(self):
        """Check if the product is on sale."""
        return self.discount_price is not None and self.discount_price < self.price
    
    def get_labels(self):
        """Get all labels associated with this product."""
        return [relation.label for relation in self.product_labels.filter(label__is_active=True).select_related('label')]
    
    def add_label(self, label):
        """Add a label to this product."""
        if isinstance(label, str):
            label, created = ProductLabel.objects.get_or_create(name=label, defaults={'display_name': label})
        
        ProductLabelRelation.objects.get_or_create(product=self, label=label)
        return label
    
    def remove_label(self, label):
        """Remove a label from this product."""
        if isinstance(label, str):
            try:
                label = ProductLabel.objects.get(name=label)
            except ProductLabel.DoesNotExist:
                return False
        
        try:
            relation = ProductLabelRelation.objects.get(product=self, label=label)
            relation.delete()
            return True
        except ProductLabelRelation.DoesNotExist:
            return False
    
    def has_label(self, label_name):
        """Check if product has a specific label."""
        return self.product_labels.filter(label__name=label_name, label__is_active=True).exists()


class ProductImage(models.Model):
    """
    Model for additional product images.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='products/')
    is_main = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Image for {self.product.name}"


class ProductReview(models.Model):
    """
    Model for product reviews and ratings.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_at',)
        unique_together = ('product', 'user')
    
    def __str__(self):
        return f"{self.user.username}'s review of {self.product.name}"


class ProductLabel(models.Model):
    """
    Model for custom product labels that can be added to products like 'Trending', 'Hot', etc.
    """
    name = models.CharField(max_length=50, unique=True)
    display_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=20, default='#FF0000')  # Default red color
    background_color = models.CharField(max_length=20, default='#FFFFFF')  # Default white background
    priority = models.PositiveSmallIntegerField(default=10)  # Higher number = higher priority
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-priority',)
    
    def __str__(self):
        return self.display_name
    
    def color_tag(self):
        """Returns a colored box representing the label's color"""
        return mark_safe(f'<div style="background-color: {self.background_color}; color: {self.color}; padding: 5px; border-radius: 3px; display: inline-block; min-width: 50px; text-align: center;">{self.display_name}</div>')
    
    color_tag.short_description = 'Preview'


class ProductLabelRelation(models.Model):
    """
    Model to associate labels with products
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_labels')
    label = models.ForeignKey(ProductLabel, on_delete=models.CASCADE, related_name='products')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('product', 'label')
        ordering = ('label__priority',)
    
    def __str__(self):
        return f"{self.product.name} - {self.label.display_name}"


class ProductVariant(models.Model):
    """
    Model for product variants such as different sizes and colors.
    """
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=50)
    sku = models.CharField(max_length=50, unique=True)
    stock = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('product', 'size', 'color')
    
    def __str__(self):
        return f"{self.product.name} - {self.size}, {self.color}"
