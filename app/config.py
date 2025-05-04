import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # RSS Feeds
    RSS_FEEDS = {
        "Nature Reviews Drug Discovery": "https://www.nature.com/nrd/current_issue/rss",
        "Nature Reviews Cancer": "https://www.nature.com/nrc/current_issue/rss",
        "Nature Biomedical Engineering": "https://www.nature.com/natbiomedeng/current_issue/rss",
        "Nature Biotechnology": "https://www.nature.com/nbt/current_issue/rss",
        "Nature Genetics": "https://www.nature.com/ng/current_issue/rss",
        "Nature": "https://www.nature.com/nature/current_issue/rss"
    }
    
    # File paths
    PREFERENCES_FILE = "preferences.txt"
    DIGEST_PATH_FMT = "digests/{date}.html"
    
    # GitHub settings
    GITHUB_REPO = os.getenv("GITHUB_REPO")
    GITHUB_BRANCH = "simple_version"
    
    # OpenAI settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-4"
    
    # Logging
    LOG_LEVEL = "INFO" 