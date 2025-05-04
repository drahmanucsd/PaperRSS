import requests

def test_rss_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Error with {url}: {str(e)}")
        return False

# Test the new feeds
new_feeds = {
    "Nature Medicine": "https://www.nature.com/nm/current_issue/rss",
    "Nature Neuroscience": "https://www.nature.com/neuro/current_issue/rss",
    "Nature Nanotechnology": "https://www.nature.com/nnano/current_issue/rss",
    "Nature Cell Biology": "https://www.nature.com/ncb/current_issue/rss"
}

print("Testing new RSS feeds...")
for journal, url in new_feeds.items():
    if test_rss_feed(url):
        print(f"✅ {journal} RSS feed is working")
    else:
        print(f"❌ {journal} RSS feed failed") 