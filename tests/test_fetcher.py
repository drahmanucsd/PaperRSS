import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from app.fetcher import fetch_today_articles, parse_date, extract_doi
from app.models import Paper

def test_paper_creation():
    """Test that Paper objects are created with correct attributes."""
    paper = Paper(
        title="Test Paper",
        doi="10.1234/test",
        link="https://nature.com/test",
        abstract="Test abstract",
        journal="Nature",
        published_date=datetime.now()
    )
    
    assert paper.title == "Test Paper"
    assert paper.doi == "10.1234/test"
    assert paper.journal == "Nature"
    assert paper.summary is None

def test_paper_doi_formatting():
    """Test that DOIs are properly formatted."""
    paper = Paper(
        title="Test Paper",
        doi="1234/test",
        link="https://nature.com/test",
        abstract="Test abstract",
        journal="Nature",
        published_date=datetime.now()
    )
    
    assert paper.doi == "10.1234/test"

def test_parse_date_with_parsed_date():
    """Test parsing date from published_parsed field."""
    entry = MagicMock()
    entry.published_parsed = (2024, 3, 15, 12, 0, 0, 0, 0, 0)
    result = parse_date(entry)
    assert result == datetime(2024, 3, 15, 12, 0, 0)

def test_parse_date_with_string_date():
    """Test parsing date from string date field."""
    entry = MagicMock()
    entry.published = "2024-03-15T12:00:00+00:00"
    result = parse_date(entry)
    assert result.date() == datetime(2024, 3, 15).date()

def test_parse_date_fallback():
    """Test date parsing fallback to current date."""
    entry = MagicMock()
    result = parse_date(entry)
    assert isinstance(result, datetime)
    assert result.date() == datetime.now().date()

def test_extract_doi_from_id():
    """Test DOI extraction from id field."""
    entry = MagicMock()
    entry.id = "https://doi.org/10.1234/test"
    result = extract_doi(entry)
    assert result == "10.1234/test"

def test_extract_doi_from_link():
    """Test DOI extraction from link field."""
    entry = MagicMock()
    entry.link = "https://nature.com/articles/10.1234/test"
    result = extract_doi(entry)
    assert result == "10.1234/test"

def test_extract_doi_fallback():
    """Test DOI extraction fallback to placeholder."""
    entry = MagicMock()
    result = extract_doi(entry)
    assert result.startswith("10.placeholder-")

def test_extract_doi():
    """Test DOI extraction from various formats."""
    from app.fetcher import extract_doi
    from datetime import datetime
    
    # Test cases
    test_cases = [
        {
            'id': 'https://doi.org/10.1038/nature12345',
            'expected': '10.1038/nature12345'
        },
        {
            'link': 'https://www.nature.com/articles/10.1038/s41586-024-12345-6',
            'expected': '10.1038/s41586-024-12345-6'
        },
        {
            'summary': 'This paper (DOI: 10.1038/nbt.1234) presents...',
            'expected': '10.1038/nbt.1234'
        },
        {
            'id': 'https://example.com/article',
            'expected': f"10.placeholder-{datetime.now().strftime('%Y%m%d')}"
        }
    ]
    
    for test_case in test_cases:
        # Create mock entry
        entry = MagicMock()
        for field, value in test_case.items():
            setattr(entry, field, value)
        
        # Test DOI extraction
        doi = extract_doi(entry)
        
        # For placeholder DOIs, only check the prefix
        if 'placeholder' in test_case['expected']:
            assert doi.startswith('10.placeholder-')
        else:
            assert doi == test_case['expected']

@patch('app.fetcher.feedparser.parse')
def test_fetch_today_articles_empty_feed(mock_parse):
    """Test handling of empty feed."""
    mock_parse.return_value.entries = []
    result = fetch_today_articles()
    assert result == []

@patch('app.fetcher.feedparser.parse')
def test_fetch_today_articles_with_valid_entry(mock_parse):
    """Test fetching articles with valid entry."""
    test_date = datetime(2024, 3, 15).date()
    
    # Create mock entry
    entry = MagicMock()
    entry.published_parsed = (2024, 3, 15, 12, 0, 0, 0, 0, 0)
    entry.get = lambda x, default=None: {
        'title': 'Test Paper',
        'link': 'https://nature.com/test',
        'summary': 'Test abstract'
    }.get(x, default)
    entry.title = "Test Paper"
    entry.id = "https://doi.org/10.1234/test"
    entry.link = "https://nature.com/test"
    entry.summary = "Test abstract"
    
    # Setup mock feed
    mock_feed = MagicMock()
    mock_feed.entries = [entry]
    mock_parse.return_value = mock_feed
    
    # Mock datetime.now() to return our test date
    mock_now = MagicMock()
    mock_now.date.return_value = test_date
    
    # Mock parse_date to return a datetime with our test date
    mock_parsed_date = datetime(2024, 3, 15, 12, 0, 0)
    with patch('app.fetcher.datetime') as mock_datetime, \
         patch('app.fetcher.Config.RSS_FEEDS', {"Nature": "https://nature.com/rss"}), \
         patch('app.fetcher.parse_date', return_value=mock_parsed_date):
        mock_datetime.now.return_value = mock_now
        result = fetch_today_articles()
        
        assert len(result) == 1
        assert isinstance(result[0], Paper)
        assert result[0].title == "Test Paper"
        assert result[0].doi == "10.1234/test"

@patch('app.fetcher.feedparser.parse')
def test_fetch_today_articles_with_old_entry(mock_parse):
    """Test that old entries are filtered out."""
    # Create mock entry with old date
    entry = MagicMock()
    entry.published_parsed = (2024, 3, 1, 12, 0, 0, 0, 0, 0)
    entry.title = "Old Paper"
    
    # Setup mock feed
    mock_feed = MagicMock()
    mock_feed.entries = [entry]
    mock_parse.return_value = mock_feed
    
    # Test with today's date
    with patch('app.fetcher.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 3, 15, 12, 0, 0)
        result = fetch_today_articles()
        
        assert len(result) == 0 