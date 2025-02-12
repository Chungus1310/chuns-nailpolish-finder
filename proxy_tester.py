import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os
import random
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "https://market.yandex.ru/search?text=%D0%BB%D0%B0%D0%BA%20%D0%B4%D0%BB%D1%8F%20%D0%BD%D0%BE%D0%B3%D1%82%D0%B5%D0%B9%20%D1%86%D0%B2%D0%B5%D1%82%D0%B0%20%D0%BC%D0%BE%D1%80%D1%81%D0%BA%D0%BE%D0%B9%20%D0%B2%D0%BE%D0%BB%D0%BD%D1%8B"
TIMEOUT = 10
working_proxies = []

def load_proxies():
    proxy_file = os.path.join(os.path.dirname(__file__), 'proxy.txt')
    try:
        with open(proxy_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error loading proxies: {e}")
        return []

def test_proxy(proxy):
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
            # Updated selector verification
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check for multiple valid selectors to ensure we got a real page
            valid_page = (
                soup.select('section._3BHKe article[data-auto="searchOrganic"]') and
                soup.select('span[data-auto="snippet-title"]') and
                soup.select('div._1ENFO a[data-auto="snippet-link"]')
            )
            
            if valid_page:
                print(f"✅ Success: {proxy} - Response time: {elapsed_time:.2f}s")
                working_proxies.append((proxy, elapsed_time))
                return True, proxy, elapsed_time
            else:
                print(f"❌ Failed: {proxy} - Invalid content received")
                return False, proxy, elapsed_time
        else:
            print(f"❌ Failed: {proxy} - Status code: {response.status_code}")
            return False, proxy, elapsed_time
            
    except Exception as e:
        print(f"❌ Failed: {proxy} - Error: {str(e)}")
        return False, proxy, None

def save_working_proxies():
    if not working_proxies:
        print("No working proxies found!")
        return
        
    # Sort by response time
    sorted_proxies = sorted(working_proxies, key=lambda x: x[1])
    
    output_file = os.path.join(os.path.dirname(__file__), 'working_proxies.txt')
    with open(output_file, 'w') as f:
        for proxy, time in sorted_proxies:
            f.write(f"{proxy} # Response time: {time:.2f}s\n")
    
    print(f"\nSaved {len(working_proxies)} working proxies to working_proxies.txt")

def main():
    proxies = load_proxies()
    if not proxies:
        print("No proxies found in proxy.txt")
        return
        
    print(f"Testing {len(proxies)} proxies...")
    print("=" * 50)
    
    # Test proxies in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_proxy = {executor.submit(test_proxy, proxy): proxy for proxy in proxies}
        for future in as_completed(future_to_proxy):
            future.result()
    
    save_working_proxies()
    
    print("\nProxy Test Summary:")
    print(f"Total proxies tested: {len(proxies)}")
    print(f"Working proxies: {len(working_proxies)}")
    print(f"Success rate: {(len(working_proxies)/len(proxies))*100:.1f}%")

if __name__ == "__main__":
    main()
