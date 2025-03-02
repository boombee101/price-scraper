import requests
from bs4 import BeautifulSoup
import time
import random


# ✅ Random User-Agent to prevent detection
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]


def get_headers():
    return {"User-Agent": random.choice(USER_AGENTS)}


def scrape_google_shopping(product_name):
    """Scrapes Google Shopping for product prices."""
    search_query = product_name.replace(" ", "+")
    google_shopping_url = f"https://www.google.com/search?tbm=shop&q={search_query}"

    print("🔎 Searching Google Shopping...")
    try:
        time.sleep(random.randint(3, 6))  # Prevents bot detection
        response = requests.get(google_shopping_url, headers=get_headers())

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            for result in soup.select('.sh-dgr__content'):
                title = result.select_one('.tAxDx').text if result.select_one('.tAxDx') else "No title"
                price = result.select_one('.a8Pemb').text if result.select_one('.a8Pemb') else "No price"
                link = result.select_one('a')['href'] if result.select_one('a') else "#"

                products.append({
                    "retailer": "Google Shopping",
                    "title": title,
                    "price": price,
                    "link": f"https://www.google.com{link}"
                })

            return products

        else:
            print(f"❌ Google Shopping request failed: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠ Google Shopping scraping error: {e}")
        return []


def scrape_walmart(product_name):
    """Scrapes Walmart for product prices."""
    search_query = product_name.replace(" ", "+")
    walmart_url = f"https://www.walmart.com/search?q={search_query}"

    print("🔎 Searching Walmart...")
    try:
        time.sleep(random.randint(3, 6))
        response = requests.get(walmart_url, headers=get_headers())

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            for item in soup.select('.search-result-gridview-item'):
                title = item.select_one('.product-title-link span').text if item.select_one('.product-title-link span') else "No title"
                price = item.select_one('.price-main .visuallyhidden').text if item.select_one('.price-main .visuallyhidden') else "No price"
                link = item.select_one('.product-title-link')['href'] if item.select_one('.product-title-link') else "#"

                products.append({
                    "retailer": "Walmart",
                    "title": title,
                    "price": price,
                    "link": f"https://www.walmart.com{link}"
                })

            return products

        else:
            print(f"❌ Walmart request failed: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠ Walmart scraping error: {e}")
        return []


def scrape_amazon(product_name):
    """Scrapes Amazon for product prices."""
    search_query = product_name.replace(" ", "+")
    amazon_url = f"https://www.amazon.com/s?k={search_query}"

    print("🔎 Searching Amazon...")
    try:
        time.sleep(random.randint(3, 6))
        response = requests.get(amazon_url, headers=get_headers())

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            products = []

            for item in soup.select('.s-result-item'):
                title = item.select_one('.a-text-normal').text if item.select_one('.a-text-normal') else "No title"
                price_whole = item.select_one('.a-price-whole').text if item.select_one('.a-price-whole') else ""
                price_fraction = item.select_one('.a-price-fraction').text if item.select_one('.a-price-fraction') else ""
                price = f"${price_whole}{price_fraction}" if price_whole else "No price"
                link = item.select_one('.a-link-normal')['href'] if item.select_one('.a-link-normal') else "#"

                products.append({
                    "retailer": "Amazon",
                    "title": title,
                    "price": price,
                    "link": f"https://www.amazon.com{link}"
                })

            return products

        else:
            print(f"❌ Amazon request failed: {response.status_code}")
            return []

    except Exception as e:
        print(f"⚠ Amazon scraping error: {e}")
        return []


def scrape_prices(product_name):
    """Scrapes multiple sources for product prices."""
    results = []

    # 🔹 Google Shopping
    google_results = scrape_google_shopping(product_name)
    results.extend(google_results)

    # 🔹 Walmart
    walmart_results = scrape_walmart(product_name)
    results.extend(walmart_results)

    # 🔹 Amazon
    amazon_results = scrape_amazon(product_name)
    results.extend(amazon_results)

    return results if results else [{"error": "⚠ No products found for this item"}]


# ✅ Test the scraper locally
if __name__ == "__main__":
    product_name = "iphone"
    results = scrape_prices(product_name)
    print(results)
