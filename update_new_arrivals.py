import re

# Read the file
with open('core/templates/core/home.html', 'r') as file:
    content = file.read()

# Create the updated content for new arrivals
new_arrivals_pattern = r'''({% if product.is_new %}
                                        <div class="badge badge-new">
                                            NEW
                                        </div>
                                    {% endif %})'''

new_arrivals_replacement = r'''{% if product.is_new %}
                                        <div class="badge badge-new">
                                            NEW
                                        </div>
                                    {% endif %}
                                    
                                    <!-- Display custom product labels on the right -->
                                    {% include "products/includes/product_card_labels.html" with product=product %}'''

# Replace new arrivals section
updated_content = re.sub(new_arrivals_pattern, new_arrivals_replacement, content, flags=re.DOTALL)

# Write the updated content back to the file
with open('core/templates/core/home.html', 'w') as file:
    file.write(updated_content)

print("Updated new arrivals section in home.html successfully")
