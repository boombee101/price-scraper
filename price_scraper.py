import requests
from bs4 import BeautifulSoup


def scrape_prices(product_name):
    """
    Scrapes product prices from Google Shopping, Walmart, and Amazon.
    Returns a list of dictionaries containing product details.
    """
    search_query = product_name.replace(" ", "+")

    # URLs for scraping
    google_shopping_url = f"https://www.google.com/search?tbm=shop&q={search_query}"
    walmart_url = f"https://www.walmart.com/search?q={search_query}"
    amazon_url = f"https://www.amazon.com/s?k={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    products = []

    # Scrape Google Shopping
    try:
        response = requests.get(google_shopping_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for result in soup.select('.sh-dgr__grid-result'):
                title = result.select_one('.Xjkr3b').text if result.select_one('.Xjkr3b') else "No title"
                price = result.select_one('.a8Pemb').text if result.select_one('.a8Pemb') else "No price"
                link = result.select_one('a')['href'] if result.select_one('a') else "#"

                products.append({
                    "retailer": "Google Shopping",
                    "title": title,
                    "price": price,
                    "link": f"https://www.google.com{link}"
                })
        else:
            print(f"❌ Google Shopping request failed: {response.status_code}")
    except Exception as e:
        print(f"⚠ Google Shopping scraping error: {e}")

    # Scrape Walmart
    try:
        response = requests.get(walmart_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.select('.search-result-gridview-item'):
                title = item.select_one('.product-title-link span').text if item.select_one(
                    '.product-title-link span') else "No title"
                price = item.select_one('.price-main span').text if item.select_one('.price-main span') else "No price"
                link = item.select_one('.product-title-link')['href'] if item.select_one('.product-title-link') else "#"

                products.append({
                    "retailer": "Walmart",
                    "title": title,
                    "price": price,
                    "link": f"https://www.walmart.com{link}"
                })
        else:
            print(f"❌ Walmart request failed: {response.status_code}")
    except Exception as e:
        print(f"⚠ Walmart scraping error: {e}")

    # Scrape Amazon
    try:
        response = requests.get(amazon_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for item in soup.select('.s-result-item'):
                title = item.select_one('.a-text-normal').text if item.select_one('.a-text-normal') else "No title"
                price = item.select_one('.a-price-whole').text if item.select_one('.a-price-whole') else "No price"
                link = item.select_one('.a-link-normal')['href'] if item.select_one('.a-link-normal') else "#"

                products.append({
                    "retailer": "Amazon",
                    "title": title,
                    "price": f"${price}" if price != "No price" else "No price",
                    "link": f"https://www.amazon.com{link}"
                })
        else:
            print(f"❌ Amazon request failed: {response.status_code}")
    except Exception as e:
        print(f"⚠ Amazon scraping error: {e}")

    return products if products else [{"error": "No products found"}]
