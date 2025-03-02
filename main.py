import os
from flask import Flask, request, jsonify
from price_scraper import scrape_prices

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Price Scraper API is running!"})

@app.route('/scrape', methods=['GET'])
def scrape():
    product_name = request.args.get('product', '')  # Get product name from URL query
    if not product_name:
        return jsonify({"error": "Please provide a product name"}), 400

    try:
        prices = scrape_prices(product_name)  # Call the scraper
        return jsonify({"product": product_name, "prices": prices})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 10000))  # Read from env, default 10000
    app.run(host='0.0.0.0', port=port)
