from bs4 import BeautifulSoup
import json
import requests
from urllib.parse import quote
import time
import random
from deep_translator import GoogleTranslator
from fake_useragent import UserAgent

def get_html_content(search_query, custom_user_agent=None):
    """
    Fetches HTML content from Yandex Market search with optional custom user agent.
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
    
    try:
        time.sleep(random.uniform(1, 3))
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
        
    except requests.RequestException as e:
        print(f"Error fetching search results: {e}")
        return None

def scrape_yandex_market_items(search_query):
    """
    Scrapes Yandex Market search results with multiple retry attempts using different user agents.
    """
    print(f"Yandex Market search query: {search_query}")
    
    # First attempt with default user agent
    html_content = get_html_content(search_query)
    products = parse_products(html_content) if html_content else []
    
    if products:
        return products
    
    print("No results with default user agent, trying with fake user agents...")
    
    # Initialize fake user agent
    try:
        ua = UserAgent()
    except Exception as e:
        print(f"Error initializing UserAgent: {e}")
        return []
    
    # Try two more times with random user agents
    for attempt in range(2):
        try:
            print(f"Attempt {attempt + 2} with fake user agent")
            random_ua = ua.random
            print(f"Using user agent: {random_ua}")
            
            time.sleep(random.uniform(2, 4))  # Add longer delay between retries
            html_content = get_html_content(search_query, random_ua)
            products = parse_products(html_content) if html_content else []
            
            if products:
                return products
                
        except Exception as e:
            print(f"Error in attempt {attempt + 2}: {e}")
            continue
    
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
            # Extract product details
            title_element = container.select_one('span[data-auto="snippet-title"]')
            price_element = container.select_one('span[data-auto="snippet-price-current"] span.ds-text_headline-5_bold')
            rating_element = container.select_one('span._1kXge span[aria-hidden="true"].ds-text_weight_med')
            reviews_element = container.select_one('span._1kXge span[aria-hidden="true"].ds-text_lineClamp_1')
            image_element = container.select_one('div._1OjQK img.w7Bf7')
            url_element = container.select_one('div._1ENFO a[data-auto="snippet-link"]')

            # Skip if missing essential elements
            if not title_element or not image_element or not url_element:
                continue

            # Format rating string to match Amazon format
            rating = None
            if rating_element:
                try:
                    rating = rating_element.text.strip()
                    rating = float(rating.replace(',', '.'))  # Convert Russian format to float
                except ValueError:
                    rating = None

            # Format review count
            reviews_count = None
            if reviews_element:
                try:
                    reviews_text = reviews_element.text.strip()
                    reviews_count = ''.join(filter(str.isdigit, reviews_text))
                except:
                    reviews_count = None

            # Create product dictionary
            product = {
                'title': title_element.text.strip(),
                'price': price_element.text.strip() if price_element else None,
                'rating': str(rating) if rating else None,
                'reviews_count': reviews_count,
                'image_url': image_element['src'],
                'product_url': 'https://market.yandex.ru' + url_element['href']
            }

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
