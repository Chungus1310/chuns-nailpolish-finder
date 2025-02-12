from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import quote
import time
import random
from deep_translator import GoogleTranslator
from fake_useragent import UserAgent
import os
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
import concurrent.futures

def load_proxies():
    """Load proxies from proxy.txt file"""
    proxy_file = os.path.join(os.path.dirname(__file__), 'proxy.txt')
    try:
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []

def get_random_proxy(proxies):
    """Get a random proxy from the list"""
    if not proxies:
        return None
    return random.choice(proxies)

def get_html_content(search_query, custom_user_agent=None, proxy=None):
    """
    Fetches HTML content from Yandex Market search with optional custom user agent and proxy.
    """
    # First translate the query to Russian
    try:
        translator = GoogleTranslator(source='en', target='ru')
        translated_query = translator.translate(search_query)
        print(f"Translated query: {translated_query}")
        
        # Then URL encode the translated query
        encoded_query = quote(translated_query)
        url = f"https://market.yandex.ru/search?text={encoded_query}"
        print(f"Search URL: {url}")
    except Exception as e:
        print(f"Translation error: {e}, using original query")
        encoded_query = quote(search_query)
        url = f"https://market.yandex.ru/search?text={encoded_query}"
    
    headers = {
        'User-Agent': custom_user_agent or 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    proxies = None
    if proxy:
        proxies = {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        print(f"Using proxy: {proxy}")
    
    try:
        time.sleep(random.uniform(0.5, 1))  # Reduced wait time
        response = requests.get(url, headers=headers, proxies=proxies, timeout=5)  # Reduced timeout
        response.raise_for_status()
        return response.text
        
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return None

def scrape_with_config(search_query, user_agent, proxy, result_queue):
    """
    Scrape function for individual thread with multiple retries
    """
    max_retries = 4
    for retry in range(max_retries):
        try:
            html_content = get_html_content(search_query, user_agent, proxy)
            if html_content:
                products = parse_products(html_content)
                if products:
                    result_queue.put(products)
                    return products
            print(f"Attempt {retry + 1} failed with proxy {proxy}, retrying...")
            time.sleep(random.uniform(1, 2))  # Wait between retries
        except Exception as e:
            print(f"Thread error (attempt {retry + 1}): {e}")
    return None

def scrape_yandex_market_items(search_query):
    """
    Scrapes Yandex Market search results using multiple threads
    """
    print(f"Yandex Market search query: {search_query}")
    
    # First attempt without proxy and custom user agent
    print("Attempting to scrape without proxy...")
    try:
        html_content = get_html_content(search_query)
        if html_content:
            products = parse_products(html_content)
            if products:
                return products
    except Exception as e:
        print(f"Initial attempt failed: {e}")
    
    print("Falling back to proxy and user agent rotation...")
    
    proxies = load_proxies()
    if not proxies:
        print("Warning: No proxies loaded")
        proxies = [None]
    
    try:
        ua = UserAgent()
    except Exception as e:
        print(f"Error initializing UserAgent: {e}")
        return []

    result_queue = Queue()
    max_threads = 6  # Fixed number of parallel threads
    
    # Prepare configurations for parallel execution
    configs = []
    for _ in range(max_threads):
        random_ua = ua.random
        random_proxy = random.choice(proxies)
        configs.append((search_query, random_ua, random_proxy))

    # Execute threads in parallel
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        futures = [
            executor.submit(scrape_with_config, *config, result_queue)
            for config in configs
        ]

        # Wait for first successful result or all failures
        try:
            for future in as_completed(futures, timeout=60):  # Increased timeout to accommodate retries
                result = future.result()
                if result:
                    # Cancel remaining futures
                    for f in futures:
                        f.cancel()
                    return result
        except concurrent.futures.TimeoutError:
            print("Scraping timed out")
        except Exception as e:
            print(f"Error in thread execution: {e}")

    # If we get here, check if we have any results in the queue
    if not result_queue.empty():
        return result_queue.get()
    
    print("All attempts failed to retrieve products")
    return []

def parse_products(html_content):
    """
    Parses HTML content and extracts product information.
    """
    if not html_content:
        return []
        
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    item_count = 0

    # Select all article elements that are not sponsored
    item_containers = soup.select('section._3BHKe article[data-auto="searchOrganic"]')

    for container in item_containers:
        if item_count >= 30:  # Get up to 30 items
            break

        try:
            # Create product dictionary with default values
            product = {
                'title': 'N/A',
                'price_current': None,
                'price_old': None,
                'discount_percentage': None,
                'rating': None,
                'reviews_count': None,
                'image_url': None,
                'product_url': None,
                'delivery_info': None
            }

            # Extract title and URL
            title_element = container.select_one('span[data-auto="snippet-title"]')
            url_element = container.select_one('div._1ENFO a[data-auto="snippet-link"]')
            if title_element and url_element:
                product['title'] = title_element.text.strip()
                product['product_url'] = 'https://market.yandex.ru' + url_element['href']
            else:
                continue  # Skip if essential elements are missing

            # Extract image URL
            image_element = container.select_one('div._1OjQK img.w7Bf7')
            if image_element:
                product['image_url'] = image_element['src']

            # Extract price information
            price_current = container.select_one('span[data-auto="snippet-price-current"] span.ds-text_headline-5_bold')
            price_old = container.select_one('span[data-auto="snippet-price-old"] span.ds-text')
            discount = container.select_one('div[data-auto="discount-badge"] span.ds-badge__textContent span:first-child')

            product['price_current'] = price_current.text.strip() if price_current else None
            product['price_old'] = price_old.text.strip() if price_old else None
            product['discount_percentage'] = discount.text.strip() if discount else None

            # Extract rating and reviews
            rating_element = container.select_one('span._1kXge span[aria-hidden="true"].ds-text_weight_med')
            reviews_element = container.select_one('span._1kXge span[aria-hidden="true"].ds-text_lineClamp_1')
            
            if rating_element:
                try:
                    rating = rating_element.text.strip()
                    product['rating'] = float(rating.replace(',', '.'))
                except ValueError:
                    pass

            if reviews_element:
                reviews_text = reviews_element.text.strip()
                product['reviews_count'] = ''.join(filter(str.isdigit, reviews_text))

            # Extract delivery information
            delivery_element = container.select_one('div[data-auto="delivery-wrapper"] span._1yLiV')
            delivery_type = container.select_one('div[data-auto="delivery-wrapper"] span._1U2DA._2Lt3J')
            delivery_extra = container.select_one('div[data-auto="delivery-wrapper"] span._1U2DA.DhcCT')

            delivery_info = []
            if delivery_element:
                delivery_info.append(delivery_element.text.strip())
            if delivery_type:
                delivery_info.append(delivery_type.text.strip())
            if delivery_extra:
                delivery_info.append(delivery_extra.text.strip())

            product['delivery_info'] = ', '.join(delivery_info) if delivery_info else None

            products.append(product)
            item_count += 1
            print(f"Processed Yandex product {item_count}: {product['title'][:50]}...")

        except Exception as e:
            print(f"Error processing product: {e}")
            continue

    print(f"\nSuccessfully scraped {len(products)} products from Yandex Market")
    return products

if __name__ == '__main__':
    search_query = "sea pink colored nail polish"  # Simple format without quotes
    products = scrape_yandex_market_items(search_query)
    if products:
        print(json.dumps(products, indent=2, ensure_ascii=False))
