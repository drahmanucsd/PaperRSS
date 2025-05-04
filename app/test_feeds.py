import requests
import feedparser
from app.config import Config
import time
import pytest

@pytest.fixture
def feed_urls():
    return Config.RSS_FEEDS

def test_feed_connection(feed_urls):
    """Test that all feeds are accessible and contain entries."""
    for journal, url in feed_urls.items():
        try:
            # Add a user agent to avoid being blocked
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Try to fetch the feed
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # Parse the feed
            feed = feedparser.parse(response.content)
            
            # Check for parsing errors
            assert not feed.bozo, f"Feed parsing error for {journal}: {feed.bozo_exception}"
            
            # Check for entries
            assert len(feed.entries) > 0, f"No entries found in feed for {journal}"
            
            # Be nice to the servers
            time.sleep(1)
            
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed for {journal}: {str(e)}")
        except Exception as e:
            pytest.fail(f"Unexpected error for {journal}: {str(e)}")

def test_feed_content(feed_urls):
    """Test that feed entries have required fields."""
    for journal, url in feed_urls.items():
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            # Check first entry for required fields
            if feed.entries:
                entry = feed.entries[0]
                # Required fields
                assert hasattr(entry, 'title'), f"Entry in {journal} missing title"
                assert hasattr(entry, 'link'), f"Entry in {journal} missing link"
                
                # Optional fields - at least one date field should be present
                has_date = any([
                    hasattr(entry, 'published'),
                    hasattr(entry, 'updated'),
                    hasattr(entry, 'pubDate'),
                    hasattr(entry, 'date'),
                    hasattr(entry, 'dc_date'),
                    hasattr(entry, 'created')
                ])
                assert has_date, f"Entry in {journal} missing any date field"
                
                # Optional but recommended fields
                if not hasattr(entry, 'summary') and not hasattr(entry, 'description'):
                    print(f"Warning: Entry in {journal} missing summary/description")
            
            time.sleep(1)
            
        except Exception as e:
            pytest.fail(f"Error checking content for {journal}: {str(e)}")

if __name__ == "__main__":
    pytest.main([__file__]) 