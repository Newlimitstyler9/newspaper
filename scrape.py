import os
from flask import Flask, request, jsonify
from newspaper import Article, Config
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Set a browser-like User-Agent
user_config = Config()
user_config.browser_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
user_config.request_timeout = 10

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        # Use the custom config to bypass 403 errors
        article = Article(url, config=user_config)
        article.download()
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
