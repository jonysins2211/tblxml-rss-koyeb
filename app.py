from flask import Flask, send_file
import threading
import os
from scraper import scrape_loop

app = Flask(__name__)

@app.route('/')
def home():
    return "✅ TamilMV RSS is live!"

@app.route('/tamilmv.xml')
def rss():
    return send_file(os.path.abspath('rss.xml'), mimetype='application/rss+xml')

@app.route('/health')
def health():
    return "OK", 200

# ✅ Ensure rss.xml exists
if not os.path.exists("rss.xml"):
    with open("rss.xml", "w", encoding="utf-8") as f:
        f.write("""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
<title>TamilBlasters Torrents</title>
<link>https://www.1tamilblasters.codes</link>
<description>Waiting for update...</description>
</channel>
</rss>""")

# ✅ Start scraper in background (only once)
def start_scraper():
    thread = threading.Thread(target=scrape_loop, daemon=True)
    thread.start()

start_scraper()

if __name__ == '__main__':
    # 🔥 IMPORTANT FIX FOR KOYEB
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
