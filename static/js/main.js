document.addEventListener('DOMContentLoaded', function() {
    // Initialize Feather Icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Mobile menu toggle
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Product quantity selector
    const quantityInputs = document.querySelectorAll('.quantity-input');
    
    quantityInputs.forEach(input => {
        const decrementBtn = input.parentNode.querySelector('.decrement-btn');
        const incrementBtn = input.parentNode.querySelector('.increment-btn');
        
        if (decrementBtn) {
            decrementBtn.addEventListener('click', () => {
                if (input.value > 1) {
                    input.value = parseInt(input.value) - 1;
                    // Trigger change event for forms that auto-submit on change
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
        
        if (incrementBtn) {
            incrementBtn.addEventListener('click', () => {
                const max = input.getAttribute('max');
                if (!max || parseInt(input.value) < parseInt(max)) {
                    input.value = parseInt(input.value) + 1;
                    // Trigger change event for forms that auto-submit on change
                    input.dispatchEvent(new Event('change'));
                }
            });
        }
    });
    
    // Product gallery / image switcher
    const productThumbnails = document.querySelectorAll('.product-thumbnail');
    const mainProductImage = document.querySelector('.main-product-image');
    
    if (productThumbnails.length && mainProductImage) {
        productThumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', () => {
                const newImageSrc = thumbnail.getAttribute('data-image');
                
                // Update main image
                mainProductImage.src = newImageSrc;
                
                // Update active state
                productThumbnails.forEach(thumb => {
                    thumb.classList.remove('active');
                });
                thumbnail.classList.add('active');
            });
        });
    }
    
    // Size and color selectors for product variants
    const variantOptions = document.querySelectorAll('.variant-option');
    
    variantOptions.forEach(option => {
        option.addEventListener('click', () => {
            // Remove selected class from siblings
            const siblingOptions = option.parentNode.querySelectorAll('.variant-option');
            siblingOptions.forEach(sibling => {
                sibling.classList.remove('selected');
                sibling.querySelector('input').checked = false;
            });
            
            // Select this option
            option.classList.add('selected');
            option.querySelector('input').checked = true;
        });
    });
    
    // Product tabs in product details page
    const productTabs = document.querySelectorAll('.product-tab');
    const productTabContents = document.querySelectorAll('.product-tab-content');
    
    if (productTabs.length && productTabContents.length) {
        productTabs.forEach(tab => {
            tab.addEventListener('click', (e) => {
                e.preventDefault();
                
                const targetId = tab.getAttribute('href').substring(1);
                
                // Hide all tab contents
                productTabContents.forEach(content => {
                    content.classList.add('hidden');
                });
                
                // Show selected tab content
                document.getElementById(targetId + '-content').classList.remove('hidden');
                
                // Update active tab
                productTabs.forEach(t => {
                    t.classList.remove('border-blue-500', 'text-blue-600');
                    t.classList.add('border-transparent', 'text-gray-500');
                });
                
                tab.classList.remove('border-transparent', 'text-gray-500');
                tab.classList.add('border-blue-500', 'text-blue-600');
            });
        });
    }
    
    // Newsletter form
    const newsletterForm = document.querySelector('form.newsletter-form');
    
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const emailInput = this.querySelector('input[type="email"]');
            const email = emailInput.value.trim();
            
            if (email) {
                // Here you would typically send the email to your backend
                // For now, we'll just show a success message
                const formContainer = this.parentNode;
                
                formContainer.innerHTML = `
                    <div class="text-center text-green-600">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto mb-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                        <h3 class="text-xl font-bold mb-2">Thank You!</h3>
                        <p>You've been successfully subscribed to our newsletter.</p>
                    </div>
                `;
            }
        });
    }
    
    // Wishlist buttons
    const wishlistButtons = document.querySelectorAll('.wishlist-button');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const isInWishlist = this.classList.contains('active');
            const productId = this.getAttribute('data-product-id');
            const url = isInWishlist 
                ? `/wishlist/remove/${productId}/` 
                : `/wishlist/add/${productId}/`;
            
            // Send AJAX request
            fetch(url, {
                method: 'GET',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    this.classList.toggle('active');
                    
                    // Update icon
                    const icon = this.querySelector('svg');
                    if (icon) {
                        if (isInWishlist) {
                            icon.classList.remove('fill-current');
                        } else {
                            icon.classList.add('fill-current');
                        }
                    }
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
    
    // Flash messages auto-dismiss
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            message.classList.add('opacity-0');
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 5000);
    });
    
    // Filter toggling for mobile
    const filterToggleBtn = document.getElementById('filter-toggle-btn');
    const filtersContainer = document.getElementById('filters-container');
    
    if (filterToggleBtn && filtersContainer) {
        filterToggleBtn.addEventListener('click', () => {
            filtersContainer.classList.toggle('hidden');
        });
    }
    
    // Product sorting
    const sortSelect = document.getElementById('sort-select');
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            // Get current URL and params
            const url = new URL(window.location.href);
            url.searchParams.set('sort', this.value);
            
            // Navigate to the new URL
            window.location.href = url.toString();
        });
    }
    
    // Rating stars in review form
    const ratingStars = document.querySelectorAll('.rating-star');
    const ratingInput = document.querySelector('input[name="rating"]');
    
    if (ratingStars.length && ratingInput) {
        ratingStars.forEach((star, index) => {
            star.addEventListener('click', () => {
                const rating = index + 1;
                ratingInput.value = rating;
                
                // Update stars UI
                ratingStars.forEach((s, i) => {
                    if (i < rating) {
                        s.classList.add('text-yellow-400');
                        s.classList.remove('text-gray-300');
                    } else {
                        s.classList.remove('text-yellow-400');
                        s.classList.add('text-gray-300');
                    }
                });
            });
        });
    }
});
