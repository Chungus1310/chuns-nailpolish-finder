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
    formatted_query = search_query.replace(' ', '+')
    url = f"https://www.amazon.com/s?k={formatted_query}"
    
    # Enhanced headers with rotating user agent
    headers = {
        'User-Agent': get_random_user_agent(),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Cache-Control': 'max-age=0',
        'dnt': '1',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'pragma': 'no-cache'
    }

    # Add session to maintain cookies
    session = requests.Session()

    try:
        print(f"Fetching results from {url}")
        print("Waiting for a few seconds before making the request...")
        time.sleep(get_random_delay())  # Random delay before request
        
        # Make the request through a session
        response = session.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        # Check if we've been redirected to a CAPTCHA page
        if 'api-services-support@amazon.com' in response.text:
            print("Amazon is requesting verification. Try:")
            print("1. Using a VPN or proxy")
            print("2. Waiting a few minutes before trying again")
            print("3. Opening the URL in a browser first")
            return []
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all product containers - using updated selectors
        products = soup.select('div[data-component-type="s-search-result"]')
        if not products:
            products = soup.select('.s-result-item')  # Alternative selector
        
        print(f"Found {len(products)} product containers")
        
        # List to store product details
        product_list = []
        count = 0
        
        # Extract details for first 20 products
        for product in products:
            if count >= 20:
                break
                
            try:
                # Extract product information
                product_data = {
                    'title': '',
                    'price': '',
                    'rating': '',
                    'reviews_count': '',
                    'image_url': '',
                    'product_url': ''
                }
                
                # Get title - multiple possible selectors
                title_element = (
                    product.select_one('h2 span.a-text-normal') or
                    product.select_one('h2.a-size-mini') or
                    product.select_one('[data-cy="title-recipe"]')
                )
                if title_element:
                    product_data['title'] = title_element.text.strip()
                
                # Get price - multiple possible selectors
                price_element = (
                    product.select_one('.a-price .a-offscreen') or
                    product.select_one('.a-price')
                )
                if price_element:
                    product_data['price'] = price_element.text.strip()
                
                # Get rating
                rating_element = product.select_one('span[aria-label*="out of 5 stars"]')
                if rating_element:
                    rating_text = rating_element.get('aria-label', '')
                    rating_match = re.search(r'([\d.]+) out of 5 stars', rating_text)
                    if rating_match:
                        product_data['rating'] = rating_match.group(1)
                
                # Get review count
                reviews_element = product.select_one('span[aria-label*="reviews"]')
                if reviews_element:
                    reviews_text = reviews_element.text.strip()
                    reviews_count = re.sub(r'[^\d]', '', reviews_text)
                    product_data['reviews_count'] = reviews_count
                
                # Get image URL
                image_element = product.select_one('img.s-image')
                if image_element:
                    product_data['image_url'] = image_element.get('src')
                
                # Get product URL
                link_element = product.select_one('a.a-link-normal[href*="/dp/"]')
                if link_element:
                    product_url = link_element.get('href')
                    if not product_url.startswith('http'):
                        product_url = 'https://www.amazon.com' + product_url
                    product_data['product_url'] = product_url
                
                # Add to product list if we have at least a title and it's not a sponsored product
                if (product_data['title'] and 
                    not product.select_one('.s-sponsored-label-info-icon') and
                    not "Sponsored" in product_data['title']):
                    product_list.append(product_data)
                    count += 1
                    print(f"Processed product {count}: {product_data['title'][:50]}...")
                
            except Exception as e:
                print(f"Error processing product: {e}")
                continue
        
        print(f"\nSuccessfully scraped {len(product_list)} products")
        return product_list
        
    except requests.RequestException as e:
        error_msg = str(e)
        if '503' in error_msg:
            print("Amazon is temporarily blocking requests. Suggestions:")
            print("1. Wait a few minutes before trying again")
            print("2. Use a VPN or proxy service")
            print("3. Try reducing the number of requests")
        else:
            print(f"Network error while scraping Amazon: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error while scraping Amazon: {e}")
        return []
    finally:
        session.close()

if __name__ == "__main__":
    search_term = "sea pink gel nail polish"
    try:
        products = scrape_amazon_products(search_term)
        if products:
            print(f"\nFound {len(products)} products")
    except KeyboardInterrupt:
        print("\nScraping interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
