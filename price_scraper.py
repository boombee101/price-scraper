import requests
from bs4 import BeautifulSoup

def scrape_prices(product_name):
    search_query = product_name.replace(" ", "+")
    google_shopping_url = f"https://www.google.com/search?tbm=shop&q={search_query}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(google_shopping_url, headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to fetch prices"}

    soup = BeautifulSoup(response.text, 'html.parser')
    products = []

    for result in soup.select('.sh-dgr__grid-result'):
        title = result.select_one('.Xjkr3b').text if result.select_one('.Xjkr3b') else "No title"
        price = result.select_one('.a8Pemb').text if result.select_one('.a8Pemb') else "No price"
        link = result.select_one('a')['href'] if result.select_one('a') else "#"

        products.append({"title": title, "price": price, "link": f"https://www.google.com{link}"})

    return products
