from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


# ✅ Google Shopping Web Scraper
def scrape_google_shopping(product_name):
    search_url = f"https://www.google.com/search?tbm=shop&q={product_name.replace(' ', '+')}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select(".sh-dgr__content")[:5]:  # Get top 5 results
        try:
            title = item.select_one(".tAxDx").text.strip()
            price = item.select_one(".a8Pemb").text.strip()
            store = item.select_one(".aULzUe").text.strip()
            link = "https://www.google.com" + item.select_one("a")["href"]
            results.append({"title": title, "price": price, "store": store, "link": link})
        except:
            continue

    return results


@app.route('/get_prices', methods=['GET'])
def get_prices():
    product_name = request.args.get('product')
    if not product_name:
        return jsonify({"error": "Missing product name"}), 400

    google_prices = scrape_google_shopping(product_name)

    return jsonify({"google_shopping": google_prices})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
