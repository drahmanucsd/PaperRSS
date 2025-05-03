import feedparser
import re
from datetime import datetime, UTC
from .models import Paper, db
from .config import Config

def extract_doi_from_content(content):
    """Extract DOI from content:encoded field."""
    if not content:
        return None
    
    # Try to find DOI in href attribute
    doi_match = re.search(r'href="https://www\.nature\.com/articles/([^"]+)"', content)
    if doi_match:
        return doi_match.group(1)
    
    # Try to find DOI in text
    doi_match = re.search(r'doi:10\.1038/([^\s<]+)', content)
    if doi_match:
        return doi_match.group(1)
    
    return None

def fetch_rss(journal_name, rss_url):
    """Fetch and parse RSS feed for a given journal."""
    print(f"Fetching {journal_name} from {rss_url}")
    
    # Try different RSS feed URLs to get a wider range of papers
    feed_urls = [
        rss_url,  # Original URL
        rss_url.replace('/rss', '/current_issue/rss'),  # Current issue
        rss_url.replace('/rss', '/journal/vaop/ncurrent/rss.rdf'),  # Articles in press
    ]
    
    all_entries = []
    for url in feed_urls:
        try:
            feed = feedparser.parse(url)
            if hasattr(feed, 'status'):
                print(f"Feed status for {url}: {feed.status}")
            if hasattr(feed, 'bozo'):
                print(f"Feed parsing error for {url}: {feed.bozo_exception if feed.bozo else 'None'}")
            
            print(f"Found {len(feed.entries)} entries from {url}")
            all_entries.extend(feed.entries)
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            continue
    
    papers = []
    
    for entry in all_entries:
        print(f"\nProcessing entry: {entry.title if hasattr(entry, 'title') else 'Unknown title'}")
        
        # Extract DOI from various possible fields
        doi = None
        
        # Try to get DOI from content:encoded field first
        if hasattr(entry, 'content'):
            print("Found content field")
            for content in entry.content:
                if content.type == 'text/html':
                    print(f"Content: {content.value[:200]}...")
                    doi = extract_doi_from_content(content.value)
                    if doi:
                        print(f"Found DOI in content: {doi}")
                        break
        
        # If not found, try content:encoded as a direct attribute
        if not doi and hasattr(entry, 'content_encoded'):
            print("Found content_encoded field")
            print(f"Content encoded: {entry.content_encoded[:200]}...")
            doi = extract_doi_from_content(entry.content_encoded)
            if doi:
                print(f"Found DOI in content_encoded: {doi}")
        
        # If still not found, try the link field
        if not doi:
            if hasattr(entry, 'id'):
                print(f"Found id field: {entry.id}")
                if "doi.org/" in entry.id:
                    doi = entry.id.split("doi.org/")[-1]
                elif "/articles/" in entry.id:
                    doi = entry.id.split("/articles/")[-1]
                elif "nature.com/articles/" in entry.id:
                    doi = entry.id.split("nature.com/articles/")[-1]
            elif hasattr(entry, 'link'):
                print(f"Found link field: {entry.link}")
                if "doi.org/" in entry.link:
                    doi = entry.link.split("doi.org/")[-1]
                elif "/articles/" in entry.link:
                    doi = entry.link.split("/articles/")[-1]
                elif "nature.com/articles/" in entry.link:
                    doi = entry.link.split("nature.com/articles/")[-1]
        
        if not doi:
            print(f"No DOI found for entry: {entry.title if hasattr(entry, 'title') else 'Unknown title'}")
            continue
            
        # Create or update paper
        paper = Paper.query.filter_by(doi=doi).first()
        if not paper:
            # Get abstract from content:encoded or other fields
            abstract = ""
            if hasattr(entry, 'content'):
                for content in entry.content:
                    if content.type == 'text/html':
                        # Extract text between </a></p> and ]]
                        match = re.search(r'</a></p>([^]]+)', content.value)
                        if match:
                            abstract = match.group(1).strip()
                            print(f"Found abstract in content: {abstract[:100]}...")
                            break
            
            if not abstract and hasattr(entry, 'content_encoded'):
                match = re.search(r'</a></p>([^]]+)', entry.content_encoded)
                if match:
                    abstract = match.group(1).strip()
                    print(f"Found abstract in content_encoded: {abstract[:100]}...")
            
            if not abstract and hasattr(entry, 'summary'):
                abstract = entry.summary
                print(f"Found abstract in summary: {abstract[:100]}...")
            elif not abstract and hasattr(entry, 'description'):
                abstract = entry.description
                print(f"Found abstract in description: {abstract[:100]}...")
            
            # Get publication date
            pub_date = datetime.now(UTC)
            if hasattr(entry, 'published_parsed'):
                pub_date = datetime(*entry.published_parsed[:6], tzinfo=UTC)
                print(f"Found publication date: {pub_date}")
            elif hasattr(entry, 'updated_parsed'):
                pub_date = datetime(*entry.updated_parsed[:6], tzinfo=UTC)
                print(f"Found update date: {pub_date}")
            
            paper = Paper(
                doi=doi,
                title=entry.title if hasattr(entry, 'title') else "Unknown title",
                journal=journal_name,
                link=entry.link if hasattr(entry, 'link') else f"https://doi.org/{doi}",
                abstract=abstract,
                impact_factor=Config.JOURNALS[journal_name]['impact_factor'],
                pub_date=pub_date
            )
            db.session.add(paper)
            print(f"Added new paper: {paper.title}")
        else:
            print(f"Found existing paper: {paper.title}")
        
        papers.append(paper)
    
    db.session.commit()
    return papers

def fetch_all_journals():
    """Fetch papers from all configured journals."""
    all_papers = []
    for journal_name, journal_info in Config.JOURNALS.items():
        try:
            papers = fetch_rss(journal_name, journal_info['rss_url'])
            all_papers.extend(papers)
        except Exception as e:
            print(f"Error fetching {journal_name}: {str(e)}")
    
    return all_papers 