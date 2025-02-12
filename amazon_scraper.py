from bs4 import BeautifulSoup
import requests
import time
import re
import random
from fake_useragent import UserAgent

def get_random_user_agent():
    ua = UserAgent()
    return ua.random

def get_random_delay():
    return random.uniform(1, 3)

def scrape_amazon_products(search_query):
    # Format the search query for URL
    terms = search_query.split()
    if terms:
        # Add quotes around the last term (item)
        terms[-1] = f'"{terms[-1]}"'
    formatted_query = '+'.join(terms)
    url = f"https://www.amazon.com/s?k={formatted_query}"
    
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0'
    }

    session = requests.Session()

    try:
        print(f"Fetching results from {url}")
        print("Waiting for a few seconds before making the request...")
        time.sleep(get_random_delay())
        
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        if 'api-services-support@amazon.com' in response.text:
            print("Amazon is requesting verification.")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        products = soup.select('div[data-component-type="s-search-result"]')
        if not products:
            products = soup.select('.s-result-item')
        
        print(f"Found {len(products)} product containers")
        
        product_list = []
        count = 0
        
        for product in products:
            if count >= 30:
                break
                
            try:
                product_data = {
                    'title': '',
                    'price': '',
                    'rating': '',
                    'reviews_count': '',
                    'image_url': '',
                    'product_url': ''
                }
                
                title_element = (
                    product.select_one('h2 span.a-text-normal') or
                    product.select_one('h2.a-size-mini') or
                    product.select_one('[data-cy="title-recipe"]')
                )
                if title_element:
                    product_data['title'] = title_element.text.strip()
                
                price_element = (
                    product.select_one('.a-price .a-offscreen') or
                    product.select_one('.a-price')
                )
                if price_element:
                    product_data['price'] = price_element.text.strip()
                
                rating_element = product.select_one('span[aria-label*="out of 5 stars"]')
                if rating_element:
                    rating_text = rating_element.get('aria-label', '')
                    rating_match = re.search(r'([\d.]+) out of 5 stars', rating_text)
                    if rating_match:
                        product_data['rating'] = rating_match.group(1)
                
                reviews_element = product.select_one('span[aria-label*="reviews"]')
                if reviews_element:
                    reviews_text = reviews_element.text.strip()
                    reviews_count = re.sub(r'[^\d]', '', reviews_text)
                    product_data['reviews_count'] = reviews_count
                
                image_element = product.select_one('img.s-image')
                if image_element:
                    product_data['image_url'] = image_element.get('src')
                
                link_element = product.select_one('a.a-link-normal[href*="/dp/"]')
                if link_element:
                    product_url = link_element.get('href')
                    if not product_url.startswith('http'):
                        product_url = 'https://www.amazon.com' + product_url
                    product_data['product_url'] = product_url
                
                if product_data['title'] and not product.select_one('.s-sponsored-label-info-icon'):
                    product_list.append(product_data)
                    count += 1
                    print(f"Processed product {count}: {product_data['title'][:50]}...")
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue

        print(f"\nSuccessfully scraped {len(product_list)} products")
        return product_list
        
    except requests.RequestException as e:
        print(f"Network error while scraping Amazon: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error while scraping Amazon: {e}")
        return []
    finally:
        session.close()

if __name__ == "__main__":
    search_term = 'laptop'  # Example search term
    try:
        products = scrape_amazon_products(search_term)
        if products:
            print(f"\nFound {len(products)} products")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
