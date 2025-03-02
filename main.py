from flask import Flask, request, jsonify
from price_scraper import scrape_prices
import os
from flask_cors import CORS  # 🔹 Enables Cross-Origin requests

app = Flask(__name__)
CORS(app)  # 🔹 Allow requests from any frontend (Flutter)


@app.route('/')
def home():
    return jsonify({"message": "✅ Price Scraper API is running!"})


@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "❌ Missing query parameter"}), 400

    try:
        # 🔹 Call the scraping function
        prices = scrape_prices(query)

        # 🔹 Handle case where no products are found
        if not prices or "error" in prices[0]:
            return jsonify({"error": "⚠ No prices found for this product"}), 404

        return jsonify({"retailers": prices})

    except Exception as e:
        print(f"🚨 API Error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # 🔹 Uses Render's assigned port
    app.run(host='0.0.0.0', port=port, debug=True)
