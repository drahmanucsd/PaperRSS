import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # RSS Feeds
    RSS_FEEDS = {
        # Nature Publishing Group
        "Nature Reviews Drug Discovery": "https://www.nature.com/nrd/current_issue/rss",
        "Nature Reviews Cancer": "https://www.nature.com/nrc/current_issue/rss",
        "Nature Biomedical Engineering": "https://www.nature.com/natbiomedeng/current_issue/rss",
        "Nature Biotechnology": "https://www.nature.com/nbt/current_issue/rss",
        "Nature Genetics": "https://www.nature.com/ng/current_issue/rss",
        "Nature": "https://www.nature.com/nature/current_issue/rss",
        "Nature Medicine": "https://www.nature.com/nm/current_issue/rss",
        "Nature Neuroscience": "https://www.nature.com/neuro/current_issue/rss",
        "Nature Nanotechnology": "https://www.nature.com/nnano/current_issue/rss",
        "Nature Cell Biology": "https://www.nature.com/ncb/current_issue/rss",
        
        # Science Family
        "Science": "https://www.science.org/rss/news_current.xml",
        
        # Cell Press
        "Cell": "https://www.cell.com/cell/current.rss",
        "Cell Stem Cell": "https://www.cell.com/cell-stem-cell/current.rss",
        "Cell Reports": "https://www.cell.com/cell-reports/current.rss",
        
        # The Lancet
        "The Lancet": "https://www.thelancet.com/rssfeed/lancet_current.xml",
        
        # Other Major Journals
        "Journal of Clinical Investigation": "https://www.jci.org/rss/current",
        
        # PLOS Journals
        "PLOS Biology": "https://journals.plos.org/plosbiology/feed/atom",
        "PLOS Medicine": "https://journals.plos.org/plosmedicine/feed/atom",
        "PLOS Computational Biology": "https://journals.plos.org/ploscompbiol/feed/atom"
    }
    
    # File paths
    PREFERENCES_FILE = "preferences.txt"
    DIGEST_PATH_FMT = "digests/{date}.html"
    
    # GitHub settings
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    GITHUB_BRANCH = "simple_version"
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4.1-mini"
    
    # Logging
    LOG_LEVEL = "INFO" 