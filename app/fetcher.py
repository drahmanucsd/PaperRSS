import logging
import feedparser
from datetime import datetime, timedelta
from typing import List
from app.models import Paper
from app.config import Config
import re

logger = logging.getLogger(__name__)

def parse_date(entry) -> datetime:
    """Parse date from feed entry using various possible fields."""
    # Try different date fields
    date_fields = ['published_parsed', 'updated_parsed', 'created_parsed']
    
    for field in date_fields:
        if hasattr(entry, field):
            try:
                return datetime(*getattr(entry, field)[:6])
            except (TypeError, ValueError):
                continue
    
    # If no parsed date found, try string dates
    date_str_fields = ['published', 'updated', 'created']
    for field in date_str_fields:
        if hasattr(entry, field):
            try:
                return datetime.strptime(getattr(entry, field), '%Y-%m-%dT%H:%M:%S%z')
            except (ValueError, TypeError):
                try:
                    return datetime.strptime(getattr(entry, field), '%Y-%m-%d')
                except (ValueError, TypeError):
                    continue
    
    # If no date found, return current date
    logger.warning(f"No date found for entry: {entry.get('title', 'Unknown')}")
    return datetime.now()

def extract_doi(entry) -> str:
    """Extract DOI from various possible locations in the entry."""
    # Try different fields that might contain DOI
    doi_fields = ['id', 'link', 'guid', 'summary']
    
    for field in doi_fields:
        if hasattr(entry, field):
            value = getattr(entry, field)
            # Look for DOI pattern in the value
            if '10.' in value:
                # Extract DOI using more precise pattern matching
                # First find the DOI pattern
                doi_pattern = r'10\.\d{4,9}/[-\w.]+[-\w.:/]+[-\w.]+'
                doi_match = re.search(doi_pattern, value, re.IGNORECASE)
                if doi_match:
                    # Clean up any trailing punctuation
                    doi = doi_match.group(0)
                    doi = re.sub(r'[.,;)]+$', '', doi)
                    return doi
    
    # If no DOI found, generate a placeholder with timestamp
    logger.warning(f"No DOI found for entry: {entry.get('title', 'Unknown')}")
    return f"10.placeholder-{datetime.now().strftime('%Y%m%d%H%M%S')}"

def fetch_today_articles() -> List[Paper]:
    """
    Fetch articles from RSS feeds published today or yesterday.
    Returns a list of Paper objects.
    """
    papers = []
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    
    for journal, feed_url in Config.RSS_FEEDS.items():
        try:
            logger.info(f"Fetching feed for {journal}")
            feed = feedparser.parse(feed_url)
            
            if not feed.entries:
                logger.warning(f"No entries found in feed for {journal}")
                continue
            
            for entry in feed.entries:
                try:
                    # Parse published date
                    published = parse_date(entry)
                    if published.date() not in [today, yesterday]:
                        continue
                    
                    # Extract DOI
                    doi = extract_doi(entry)
                    
                    # Create Paper object
                    paper = Paper(
                        title=entry.get('title', 'No Title'),
                        doi=doi,
                        link=entry.get('link', ''),
                        abstract=entry.get('summary', 'No abstract available'),
                        journal=journal,
                        published_date=published
                    )
                    papers.append(paper)
                    logger.info(f"Added paper: {paper.title}")
                    
                except Exception as e:
                    logger.error(f"Error processing entry: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error fetching feed {journal}: {str(e)}")
            continue
    
    logger.info(f"Total papers fetched: {len(papers)}")
    return papers 