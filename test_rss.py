import requests
import pytest
from app.config import Config

@pytest.fixture
def feed_urls():
    return Config.RSS_FEEDS

def test_rss_feed_connection(feed_urls):
    """Test that all RSS feeds are accessible."""
    for journal, url in feed_urls.items():
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            assert response.status_code == 200, f"Failed to access {journal} feed"
        except Exception as e:
            pytest.fail(f"Error with {journal} feed: {str(e)}")

def test_rss_feed_content(feed_urls):
    """Test that RSS feeds return valid content."""
    for journal, url in feed_urls.items():
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Check content type
            content_type = response.headers.get('content-type', '').lower()
            assert any(t in content_type for t in ['xml', 'rss', 'atom']), f"Invalid content type for {journal}: {content_type}"
            
            # Check content length
            assert len(response.content) > 0, f"Empty response from {journal} feed"
            
        except Exception as e:
            pytest.fail(f"Error checking content for {journal}: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__]) 