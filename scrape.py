import os
import time
import requests
from flask import Flask, request, jsonify
from newspaper import Article
from flask_cors import CORS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
CORS(app)

def fetch_html_with_selenium(url):
    """Fetches the page using Selenium to bypass bot detection"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)
        time.sleep(3)  # Allow time for JavaScript to load
        html = driver.page_source
        return html
    finally:
        driver.quit()

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        html = fetch_html_with_selenium(url)  # Fetch the page using Selenium
        if not html:
            return jsonify({"error": "Failed to load page with Selenium"}), 500

        article = Article(url)
        article.set_html(html)  # Pass the retrieved HTML
        article.parse()

        return jsonify({
            "title": article.title,
            "text": article.text,
            "authors": article.authors,
            "publish_date": str(article.publish_date) if article.publish_date else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
