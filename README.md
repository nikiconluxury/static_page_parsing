# Brand Site Parsing Template

This repository contains a template designed for parsing static category pages of brand websites. It is structured to be easily adaptable for different brands by following the instructions below.

## Getting Started

1. **Fork the Template**:
   - Create a fork of this repository for each new brand you wish to parse.

2. **Customize for the Brand**:
   - Rename the `BrandNameParser` class to a name specific to the brand (e.g., `AdidasParser`).
   - In the `__init__` method, replace `brand_name_here` with the actual brand name. This will help in organizing outputs and internal handling specific to the brand.

## Customize Parsing Logic

The main customization for each brand should occur within the `parse_product_blocks` method. This should be the only section of the code you edit:

### Steps for Customizing `parse_product_blocks`:

1. **Update Product Selector**:
   - Adjust the selector used to find product blocks to match the HTML structure of the specific brand's website.

2. **Extract and Format Data**:
   - For each product, extract necessary fields such as name, ID, URL, and prices.
   - Ensure names are formatted with dashes instead of spaces and converted to lowercase.

3. **Compile Data**:
   - Append each set of product data to a list which will then be included in the master list of product data.

```python
def parse_product_blocks(self, soup, category):
    # Select all elements with the class 'product-tile' that contain product details
    product_blocks = soup.select('.product-tile')
    # Print the count of product blocks found to help in debugging and verifying parsing accuracy
    print(len(product_blocks))

    # Initialize a list to store parsed product data
    parsed_data = []
    # Define the headers for the data to be stored, these will correspond to the details extracted from each product
    column_names = ['category', 'name', 'product_id', 'product_url', 'image_url', 'full_price', 'discount_price']
    # Add the column headers as the first row of the parsed_data list
    parsed_data.append(column_names)

    # Iterate through each product block to extract and parse data
    for product in product_blocks:
        # Extract the product name, handle cases where it might be absent
        name = product.select_one('.product-name a').text.strip() if product.select_one('.product-name a') else None
        # Retrieve a unique identifier for the product, usually stored as a data attribute
        product_id = product.get('data-itemid')
        # Extract the URL for the product details page
        product_url = product.select_one('.product-name a').get('href') if product.select_one('.product-name a') else None
        # Handle the extraction of the main product image URL from a possibly differently named data attribute
        image_url_tag = product.select_one('.js-producttile_image')
        image_url = image_url_tag.get('data-main-src') if image_url_tag else None
        # Extract the standard price, ensure to strip any extra whitespace
        price = product.select_one('.product-standard-price').text.strip() if product.select_one('.product-standard-price') else None
        # Look for a discount price tag and extract it, handle cases where it might be absent
        discount_price_tag = product.select_one('.product-discount-price')
        discount_price = discount_price_tag.text.strip() if discount_price_tag else None

        # Compile all the extracted data into a list
        product_data = [
            category, name, product_id, product_url, image_url, price, discount_price
        ]
        # Append the product data list to the main parsed_data list
        parsed_data.append(product_data)

    # Return the list of lists containing all the product data; this structure is important for correctly writing to a CSV file
    return parsed_data


## Running the Parser

After customizing the `parse_product_blocks` method for the specific brand:

- Run the parser using `run_parser.py`.
- Ensure that the output correctly writes to the designated output folder, formatted according to the specified fields.
