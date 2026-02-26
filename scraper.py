import time, json, requests, os
from feedgen.feed import FeedGenerator
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

FORUMS = [
    "https://www.1tamilblasters.com/index.php?/forums/forum/8-tamil-new-movies-tcrip-dvdscr-hdcam-predvd.xml",
    "https://www.1tamilblasters.com/index.php?/forums/forum/7-tamil-new-movies-hdrips-bdrips-dvdrips-hdtv.xml",
]

BASE_URL = "https://www.1tamilblasters.codes"
SEEN_FILE = "seen.json"
RSS_FILE = "rss.xml"
INTERVAL = 60

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

# Load seen
try:
    with open(SEEN_FILE) as f:
        seen = set(json.load(f))
except:
    seen = set()

def generate_rss():
    fg = FeedGenerator()
    fg.title("TamilBlasters Torrents")
    fg.link(href=BASE_URL, rel="alternate")
    fg.description("Live RSS from TamilBlasters")

    updated = False

    for forum_url in FORUMS:
        try:
            print("Checking:", forum_url)
            res = requests.get(forum_url, headers=HEADERS, timeout=30)

            if res.status_code != 200:
                print("Blocked:", res.status_code)
                continue

            root = ET.fromstring(res.content)

            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text

                if link not in seen:
                    seen.add(link)
                    fe = fg.add_entry()
                    fe.title(title)
                    fe.link(href=link)
                    fe.pubDate(time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime()))
                    print("✅ Added:", title)
                    updated = True

        except Exception as e:
            print("❌ Forum error:", e)

    fg.rss_file(RSS_FILE)

    if updated:
        with open(SEEN_FILE, "w") as f:
            json.dump(list(seen), f)
        print("🎯 RSS Updated")

def scrape_loop():
    while True:
        try:
            generate_rss()
        except Exception as e:
            print("❌ Scraper crashed:", e)
        time.sleep(INTERVAL)
