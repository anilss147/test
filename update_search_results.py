import re

# Read the file
with open('products/templates/products/search_results.html', 'r') as file:
    content = file.read()

# Create the updated content for search results
search_pattern = r'''({% if product.discount_price %}
                                        <div class="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                                            SALE
                                        </div>
                                    {% elif product.is_new %}
                                        <div class="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                                            NEW
                                        </div>
                                    {% endif %})'''

search_replacement = r'''{% if product.discount_price %}
                                        <div class="absolute top-2 left-2 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded">
                                            SALE
                                        </div>
                                    {% elif product.is_new %}
                                        <div class="absolute top-2 left-2 bg-green-500 text-white text-xs font-bold px-2 py-1 rounded">
                                            NEW
                                        </div>
                                    {% endif %}
                                    
                                    <!-- Display custom product labels on the right -->
                                    {% include "products/includes/product_card_labels.html" with product=product %}'''

# Replace search results section
updated_content = re.sub(search_pattern, search_replacement, content, flags=re.DOTALL)

# Write the updated content back to the file
with open('products/templates/products/search_results.html', 'w') as file:
    file.write(updated_content)

print("Updated search_results.html successfully")
