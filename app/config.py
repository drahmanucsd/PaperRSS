import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API domain for feedback links
    API_DOMAIN = os.environ.get('API_DOMAIN', '127.0.0.1:5001')
    
    # Journal RSS feeds
    JOURNALS = {
        'Nature Reviews Drug Discovery': {
            'rss_url': 'https://www.nature.com/nrd.rss',
            'impact_factor': 122.7
        },
        'Nature Reviews Cancer': {
            'rss_url': 'https://www.nature.com/nrc.rss',
            'impact_factor': 72.5
        },
        'Nature Biomedical Engineering': {
            'rss_url': 'https://www.nature.com/natbiomedeng.rss',
            'impact_factor': 27.7
        },
        'Nature Biotechnology': {
            'rss_url': 'https://www.nature.com/nbt.rss',
            'impact_factor': 33.1
        },
        'Nature Genetics': {
            'rss_url': 'https://www.nature.com/ng.rss',
            'impact_factor': 31.8
        },
        'Nature': {
            'rss_url': 'https://www.nature.com/nature.rss',
            'impact_factor': 50.5
        }
    }
    
    # Email settings
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
    EMAIL_FROM = os.environ.get('EMAIL_FROM')
    EMAIL_RECIPIENTS = os.environ.get('EMAIL_RECIPIENTS', '').split(',')
    
    # OpenAI settings
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
    # GitHub settings
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')
    GITHUB_REPO = os.environ.get('GITHUB_REPO') 