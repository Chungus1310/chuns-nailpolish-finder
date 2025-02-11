import os
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

    products = scrape_amazon_products(query)
    return jsonify(products[:18])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
