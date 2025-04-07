import re

# Read the file
with open('core/templates/core/home.html', 'r') as file:
    content = file.read()

# Create the updated content for featured products
featured_pattern = r'''({% if product.discount_price %}
                                        <div class="badge badge-sale">
                                            SALE
                                        </div>
                                    {% endif %}
                                    
                                    {% if product.is_new %}
                                        <div class="badge badge-new">
                                            NEW
                                        </div>
                                    {% endif %})'''

featured_replacement = r'''{% if product.discount_price %}
                                        <div class="badge badge-sale">
                                            SALE
                                        </div>
                                    {% endif %}
                                    
                                    {% if product.is_new %}
                                        <div class="badge badge-new">
                                            NEW
                                        </div>
                                    {% endif %}
                                    
                                    <!-- Display custom product labels on the right -->
                                    {% include "products/includes/product_card_labels.html" with product=product %}'''

# Replace featured products section
updated_content = re.sub(featured_pattern, featured_replacement, content, flags=re.DOTALL)

# Write the updated content back to the file
with open('core/templates/core/home.html', 'w') as file:
    file.write(updated_content)

print("Updated home.html successfully")
