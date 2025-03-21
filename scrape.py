import os
from flask import Flask, request, jsonify
from newspaper import Article
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/scrape', methods=['GET'])
def scrape():
    url = request.args.get('url')
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    try:
        article = Article(url)
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
