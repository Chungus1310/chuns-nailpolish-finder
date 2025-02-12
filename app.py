from flask import Flask, render_template, request, jsonify
from amazon_scraper import scrape_amazon_products
from yandex_scraper import scrape_yandex_market_items

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    marketplace = request.args.get("market", "amazon").strip().lower()

    if not query:
        return jsonify({"error": "Missing search query."}), 400

    if marketplace not in ["amazon", "yandex"]:
        return jsonify({"error": "Invalid marketplace selected."}), 400

    try:
        # Choose scraper based on marketplace
        if marketplace == "amazon":
            products = scrape_amazon_products(query)
        else:  # yandex
            products = scrape_yandex_market_items(query)

        # Return only the first 18 products
        return jsonify(products[:18])

    except Exception as e:
        return jsonify({
            "error": f"Error searching {marketplace}: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
