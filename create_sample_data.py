import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing_store.settings')
django.setup()

from django.contrib.auth.models import User
from products.models import Category, Product, ProductVariant, ProductImage
from django.utils.text import slugify
from decimal import Decimal

def create_sample_data():
    # Create categories
    print("Creating categories...")
    
    # Parent categories
    men, men_created = Category.objects.get_or_create(
        slug="men",
        defaults={
            "name": "Men",
            "description": "Men's clothing"
        }
    )
    if men_created:
        print("Created Men category")
    else:
        print("Men category already exists")
        
    women, women_created = Category.objects.get_or_create(
        slug="women",
        defaults={
            "name": "Women",
            "description": "Women's clothing"
        }
    )
    if women_created:
        print("Created Women category")
    else:
        print("Women category already exists")
        
    kids, kids_created = Category.objects.get_or_create(
        slug="kids",
        defaults={
            "name": "Kids",
            "description": "Kids' clothing"
        }
    )
    if kids_created:
        print("Created Kids category")
    else:
        print("Kids category already exists")
    
    # Sub-categories for Men
    Category.objects.get_or_create(
        slug="men-t-shirts", 
        defaults={
            "name": "T-Shirts", 
            "description": "Men's T-Shirts", 
            "parent": men
        }
    )
    Category.objects.get_or_create(
        slug="men-jeans", 
        defaults={
            "name": "Jeans", 
            "description": "Men's Jeans", 
            "parent": men
        }
    )
    Category.objects.get_or_create(
        slug="men-shirts", 
        defaults={
            "name": "Shirts", 
            "description": "Men's Shirts", 
            "parent": men
        }
    )
    
    # Sub-categories for Women
    Category.objects.get_or_create(
        slug="women-dresses", 
        defaults={
            "name": "Dresses", 
            "description": "Women's Dresses", 
            "parent": women
        }
    )
    Category.objects.get_or_create(
        slug="women-tops", 
        defaults={
            "name": "Tops", 
            "description": "Women's Tops", 
            "parent": women
        }
    )
    Category.objects.get_or_create(
        slug="women-jeans", 
        defaults={
            "name": "Jeans", 
            "description": "Women's Jeans", 
            "parent": women
        }
    )
    
    # Sub-categories for Kids
    Category.objects.get_or_create(
        slug="kids-boys", 
        defaults={
            "name": "Boys", 
            "description": "Boys' clothing", 
            "parent": kids
        }
    )
    Category.objects.get_or_create(
        slug="kids-girls", 
        defaults={
            "name": "Girls", 
            "description": "Girls' clothing", 
            "parent": kids
        }
    )
    
    # Create products
    print("Creating products...")
    
    # Men's products
    men_tshirt_category = Category.objects.get(slug="men-t-shirts")
    men_jeans_category = Category.objects.get(slug="men-jeans")
    men_shirts_category = Category.objects.get(slug="men-shirts")
    
    # Create Men's T-shirts
    create_product(
        name="Classic Cotton T-Shirt",
        category=men_tshirt_category,
        description="A comfortable classic cotton t-shirt for everyday wear.",
        price=Decimal("24.99"),
        discount_price=Decimal("19.99"),
        stock=100,
        gender="men",
        is_featured=True,
        is_new=True
    )
    
    create_product(
        name="V-Neck Sport T-Shirt",
        category=men_tshirt_category,
        description="Moisture-wicking V-neck t-shirt, perfect for sports and workouts.",
        price=Decimal("29.99"),
        discount_price=None,
        stock=75,
        gender="men",
        is_featured=False,
        is_new=True
    )
    
    # Create Men's Jeans
    create_product(
        name="Slim Fit Denim Jeans",
        category=men_jeans_category,
        description="Modern slim fit jeans with a classic 5-pocket design.",
        price=Decimal("59.99"),
        discount_price=None,
        stock=50,
        gender="men",
        is_featured=True,
        is_new=False
    )
    
    create_product(
        name="Relaxed Fit Jeans",
        category=men_jeans_category,
        description="Comfortable relaxed fit jeans with a straight leg.",
        price=Decimal("54.99"),
        discount_price=Decimal("49.99"),
        stock=60,
        gender="men",
        is_featured=False,
        is_new=False
    )
    
    # Create Men's Shirts
    create_product(
        name="Button-Down Oxford Shirt",
        category=men_shirts_category,
        description="Classic button-down Oxford shirt for a smart casual look.",
        price=Decimal("49.99"),
        discount_price=None,
        stock=40,
        gender="men",
        is_featured=True,
        is_new=False
    )
    
    # Women's products
    women_dresses_category = Category.objects.get(slug="women-dresses")
    women_tops_category = Category.objects.get(slug="women-tops")
    women_jeans_category = Category.objects.get(slug="women-jeans")
    
    # Create Women's Dresses
    create_product(
        name="Floral Summer Dress",
        category=women_dresses_category,
        description="Light and breezy floral dress, perfect for summer days.",
        price=Decimal("69.99"),
        discount_price=Decimal("59.99"),
        stock=30,
        gender="women",
        is_featured=True,
        is_new=True
    )
    
    create_product(
        name="Elegant Cocktail Dress",
        category=women_dresses_category,
        description="Elegant cocktail dress for special occasions and events.",
        price=Decimal("89.99"),
        discount_price=None,
        stock=25,
        gender="women",
        is_featured=True,
        is_new=False
    )
    
    # Create Women's Tops
    create_product(
        name="Casual Blouse",
        category=women_tops_category,
        description="Lightweight casual blouse that pairs well with any bottom.",
        price=Decimal("34.99"),
        discount_price=None,
        stock=45,
        gender="women",
        is_featured=False,
        is_new=True
    )
    
    # Create Women's Jeans
    create_product(
        name="High-Waisted Skinny Jeans",
        category=women_jeans_category,
        description="Flattering high-waisted skinny jeans that go with everything.",
        price=Decimal("64.99"),
        discount_price=Decimal("54.99"),
        stock=55,
        gender="women",
        is_featured=True,
        is_new=False
    )
    
    # Kids products
    boys_category = Category.objects.get(slug="kids-boys")
    girls_category = Category.objects.get(slug="kids-girls")
    
    # Create Boys' clothing
    create_product(
        name="Boys Graphic T-Shirt",
        category=boys_category,
        description="Fun graphic t-shirt for boys with playful designs.",
        price=Decimal("19.99"),
        discount_price=None,
        stock=70,
        gender="kids",
        is_featured=False,
        is_new=True
    )
    
    # Create Girls' clothing
    create_product(
        name="Girls Sparkle T-Shirt",
        category=girls_category,
        description="Sparkly t-shirt with fun design, perfect for little girls.",
        price=Decimal("22.99"),
        discount_price=Decimal("18.99"),
        stock=65,
        gender="kids",
        is_featured=True,
        is_new=True
    )
    
    print("Sample data created successfully!")

def create_product(name, category, description, price, discount_price, stock, gender, is_featured, is_new):
    """Helper function to create a product with variants."""
    slug = slugify(name)
    
    # Check if product already exists
    if Product.objects.filter(slug=slug).exists():
        print(f"Product '{name}' already exists, skipping")
        return Product.objects.get(slug=slug)
    
    product = Product(
        name=name,
        slug=slug,
        category=category,
        description=description,
        price=price,
        discount_price=discount_price,
        image="products/placeholder.svg",  # Would be replaced by actual images in production
        stock=stock,
        available=True,
        is_featured=is_featured,
        is_new=is_new,
        gender=gender
    )
    product.save()
    
    # Create variants
    sizes = ["S", "M", "L", "XL"] if gender != "kids" else ["2T", "3T", "4T", "5T"]
    colors = ["Black", "White", "Blue", "Red"]
    
    for size in sizes:
        for color in colors:
            sku = f"{slugify(name)}-{size}-{slugify(color)}"
            variant_stock = stock // (len(sizes) * len(colors))
            
            # Check if variant already exists
            if not ProductVariant.objects.filter(product=product, size=size, color=color).exists():
                ProductVariant.objects.create(
                    product=product,
                    size=size,
                    color=color,
                    sku=sku,
                    stock=variant_stock
                )
    
    print(f"Created product: {name}")
    return product

if __name__ == "__main__":
    create_sample_data()