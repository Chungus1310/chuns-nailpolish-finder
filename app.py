from flask import Flask, render_template, request, jsonify
from amazon_scraper import scrape_amazon_products

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify({"error": "Missing search query."}), 400

    # Call the scraper and return 18 products (increased from 12)
    products = scrape_amazon_products(query)
    return jsonify(products[:18])

if __name__ == '__main__':
    app.run(debug=True, port=5000)
