from main_parser import WebsiteParser
from urllib.parse import urljoin
import re

class BrandNameParser(WebsiteParser):

    def __init__(self, directory):

        self.brand = 'brand_name_here'  # Replace with brand name
        self.directory = directory

    #THIS WILL BE EDITED FOR EACH BRAND. THIS SHOULD BE THE ONLY CODE BEING UPDATED. MUST BE NAMED parse_product_blocks
    def parse_product_blocks(self,soup,category):

        ##SELECT ALL BLOCKS FIRST
        product_blocks = soup.select('.product-tile')
        print(len(product_blocks))
        parsed_data = []
        #ADD HEADER ROW TO LIST
        column_names = [
            'category', 'name', 'product_id', 'product_url', 'image_url','full_price','discount_price']
        parsed_data.append(column_names)

        #ITERATE AND PARSE
        for product in product_blocks:
            name = product.select_one(
               '.product-name a').text.strip() if product.select_one('.product-name a') else None
            product_id = product.get('data-itemid')
            product_url = product.select_one(
               '.product-name a').get('href') if product.select_one('.product-name a') else None
            image_url_tag = product.select_one('.js-producttile_image')
            image_url = image_url_tag.get(
               'data-main-src') if image_url_tag else None
            price = product.select_one('.product-standard-price').text.strip(
            ) if product.select_one('.product-standard-price') else None
            discount_price_tag = product.select_one('.product-discount-price')
            discount_price = discount_price_tag.text.strip() if discount_price_tag else None
            product_data = [
               category,
               name,
                product_id,
              product_url,
              image_url,
             price,
          discount_price,
            ]
            parsed_data.append(product_data)
        #Must return list of lists containing product data to properly write to csv.
        return parsed_data


class BurberryParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = "burberry"
        self.directory = directory
        
    def parse_product_blocks(self, soup, category):
    
        product_blocks = soup.select('a.product-card-v2-anchor, a.redesigned-product-card__link')
        print(len(product_blocks))
        parsed_data = []
        
        column_names = [
            'category', 'name',  'product_id', 'product_url', 'image_url','full_price','discount_price','tag(s)']
            
        parsed_data.append(column_names)
        
        base_url = soup.find('meta',{'property':'org:url'})
        if base_url:
            base_url = base_url['content']
        else:
           base_url = "https://us.burberry.com/"
         
        for product in product_blocks:  
        
            name = product.select_one('.product-card-v2-title, .product-card-content__title').get_text(strip=True)
            
            product_link = urljoin(base_url,product['href'])
            
            product_id = re.search('\-p(\d+)/?$',product_link,flags=re.I)
            product_id = product_id.group(1) if product_id else "unavailable"
                
            price = product.select_one('.product-card-price__current-price, .product-card-v2-price__current').get_text(strip=True)
            
            discount_price = "" #empty for now and can be added later if found
            
            image_url = product.select_one('.redesigned-product-card__picture img, .product-card-v2-carousel-container__media__picture img')['src']
            
            tags = product.select_one('.product-card-labels__flag, .product-card-v2-carousel-labels__label')
            tags = tags.get_text(strip=True) if tags else ""
                  
            product_data = [
                category,
                name,
                product_id,
                product_link,
                image_url,
                price,
                discount_price,
                tags
            ]
            
            parsed_data.append(product_data)
            
        return parsed_data          
        