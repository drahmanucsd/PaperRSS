import feedparser
from datetime import datetime
from .models import Paper, db
from .config import Config

def fetch_rss(journal_name, rss_url):
    """Fetch and parse RSS feed for a given journal."""
    feed = feedparser.parse(rss_url)
    papers = []
    
    for entry in feed.entries:
        # Extract DOI from link
        doi = entry.link.split("doi.org/")[-1] if "doi.org/" in entry.link else None
        if not doi:
            continue
            
        # Create or update paper
        paper = Paper.query.filter_by(doi=doi).first()
        if not paper:
            paper = Paper(
                doi=doi,
                title=entry.title,
                journal=journal_name,
                link=entry.link,
                abstract=entry.summary,
                impact_factor=Config.JOURNALS[journal_name]['impact_factor'],
                pub_date=datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.utcnow()
            )
            db.session.add(paper)
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