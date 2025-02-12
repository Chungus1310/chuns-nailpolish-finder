import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "https://market.yandex.ru/search?text=%D0%BB%D0%B0%D0%BA%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%BE%D0%B3%D1%82%D0%B5%D0%B9%20%D1%86%D0%B2%D0%B5%D1%82%D0%B0%20%D0%BC%D0%BE%D1%80%D1%81%D0%BA%D0%BE%D0%B9%20%D0%B2%D0%BE%D0%BB%D0%BD%D1%8B"
TIMEOUT = 10

def load_proxies():
    proxy_file = os.path.join(os.path.dirname(__file__), 'proxy.txt')
    try:
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []

def test_proxy(proxy):
    """Test a single proxy and return result only if it works"""
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    proxies = {
        'http': f'http://{proxy}',
        'https': f'http://{proxy}'
    }
    
    try:
        start_time = time.time()
        response = requests.get(
            TEST_URL,
            headers=headers,
            proxies=proxies,
            timeout=TIMEOUT
        )
        elapsed_time = time.time() - start_time
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            valid_page = (
                soup.select('section._3BHKe article[data-auto="searchOrganic"]') and
                soup.select('span[data-auto="snippet-title"]') and
                soup.select('div._1ENFO a[data-auto="snippet-link"]')
            )
            
            if valid_page:
                print(f"✅ Success: {proxy} - Response time: {elapsed_time:.2f}s")
                return {'proxy': proxy, 'time': elapsed_time}
            
        print(f"❌ Failed: {proxy} - Invalid content or status")
        return None
            
    except Exception as e:
        print(f"❌ Failed: {proxy} - Error: {str(e)}")
        return None

def save_working_proxies(working_proxies):
    """Save only the working proxies to file"""
    if not working_proxies:
        print("No working proxies found!")
        return
        
    # Sort by response time
    sorted_proxies = sorted(working_proxies, key=lambda x: x['time'])
    
    output_file = os.path.join(os.path.dirname(__file__), 'working_proxies.txt')
    with open(output_file, 'w') as f:
        for proxy_data in sorted_proxies:
            f.write(f"{proxy_data['proxy']} # Response time: {proxy_data['time']:.2f}s\n")
    
    print(f"\nSaved {len(working_proxies)} working proxies to working_proxies.txt")

def main():
    proxies = load_proxies()
    if not proxies:
        print("No proxies found in proxy.txt")
        return
        
    print(f"Testing {len(proxies)} proxies...")
    print("=" * 50)
    
    working_proxies = []
    
    # Test proxies in parallel
    with ThreadPoolExecutor(max_workers=200) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            result = future.result()
            if result:  # Only add working proxies
                working_proxies.append(result)
    
    save_working_proxies(working_proxies)
    
    print("\nProxy Test Summary:")
    print(f"Total proxies tested: {len(proxies)}")
    print(f"Working proxies: {len(working_proxies)}")
    print(f"Success rate: {(len(working_proxies)/len(proxies))*100:.1f}%")

if __name__ == "__main__":
    main()
