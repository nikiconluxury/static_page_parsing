from main_parser import WebsiteParser
from urllib.parse import urljoin, urlunparse
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
        
        
        
class KenzoParser(WebsiteParser):

    def __init__(self, directory):
        self.brand = "kenzo"
        self.directory = directory
        
    def parse_product_blocks(self, soup, category):
    
        product_blocks = soup.select("div[is='m-product-tile']")
        print(len(product_blocks))
        parsed_data = []
        
        column_names = [
            'category', 'name',  'product_id', 'product_url', 'image_url','other_images','full_price','discount_price','stock','color','tag(s)']
            
        parsed_data.append(column_names)
        
        base_url = soup.find('meta',{'property':'org:url'})
        if base_url:
            base_url = base_url['content']
            base_url = urlunparse(urlparse(base_url)[:3] + ('', '', ''))
        else:
           base_url = "https://www.kenzo.com/"
         
        for product in product_blocks:  
        
            name = product.select_one('a[class*="title t-body-bold t-plain"]').get_text(strip=True)
            
            product_link = product.select_one('a[class*="title t-body-bold t-plain"]')
            product_link = urljoin(base_url,product_link['href'])
            
            product_id = product['data-pid'] if product.get('data-pid') else "unavailable"
           
            price = product.select_one('.prices .price-sales, .prices .price').get_text(strip=True).lower()
            price = re.sub('price\s+reduced\s+from','',price,flags=re.I|re.S).replace('to','').strip()
            
            discount_price = product.select_one('.prices .reduced-price')
            discount_price = discount_price.get_text(strip=True) if discount_price else ""
            
            all_images = []
            for img in product.select("[is='m-tile-images'] img"):
                image_url = self.get_biggest_image_srcset(img)
                if image_url and image_url not in all_images:
                    all_images.append(image_url)
            
            image_url = all_images[0] if all_images else ""
            
            other_images = ' , '.join(all_images[1:]) if len(all_images)>1 else ""
            
            
            stock_status = product.select_one('.stock-state')
            stock_status = stock_status.get('aria-label') or stock_status.get_text(strip=True) if stock_status else ""
            
            colors_ul = product.select_one('ul[is="m-tile-color"]')
            if colors_ul:
                colors = [li.find('button')['aria-label'] for li in colors_ul.select('li') if li.find('button')]
                colors = [re.sub('color\s+product','',color,flags=re.I).strip() for color in colors]
                colors = [color for color in colors if color]
                if colors and colors_ul.select_one('.more-color'):
                    colors.append(colors_ul.select_one('.more-color').get_text(strip=True)+" more")
                colors = ', '.join(colors)
            else:
                colors = ""
                
            tags = product.select_one('[is="m-product-tag"]')
            tags = tags.get_text(strip=True) if tags else ""
                  
            product_data = [
                category,
                name,
                product_id,
                product_link,
                image_url,
                other_images,
                price,
                discount_price,
                stock_status,
                colors,
                tags
            ]
            
            parsed_data.append(product_data)
            
        return parsed_data          
        
    def get_biggest_image_srcset(self, img_tag):
        if not img_tag or 'srcset' not in img_tag.attrs:
            if img_tag and img_tag.get('src'):
                return img_tag['src']
            return None

        srcset = img_tag['srcset']
        srcset_entries = srcset.split(',')

        images = []
        for entry in srcset_entries:
            parts = entry.strip().split(' ')
            url = parts[0]
            if len(parts) > 1:
                descriptor = parts[1]
                if descriptor.endswith('w'):
                    width = int(descriptor[:-1])
                    images.append((width, url))
                elif descriptor.endswith('x'):
                    density = float(descriptor[:-1])
                    width = density * 1920
                    images.append((width, url))
                else:
                    continue
            else:
                images.append((1920, url))

        if not images:
            return None

        biggest_image_url = max(images, key=lambda x: x[0])[1]
        return biggest_image_url