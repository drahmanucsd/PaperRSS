import pytest
from datetime import datetime
from app.models import Paper
from app.ranker import load_preferences, rank_papers

def test_load_preferences():
    """Test loading preferences from file."""
    preferences = load_preferences()
    assert isinstance(preferences, dict)
    assert all(isinstance(weight, int) for weight in preferences.values())
    assert all(1 <= weight <= 10 for weight in preferences.values())

def test_rank_papers_empty():
    """Test ranking with empty paper list."""
    papers = []
    ranked = rank_papers(papers)
    assert ranked == []

def test_rank_papers_single():
    """Test ranking with single paper."""
    paper = Paper(
        title="Test Paper",
        doi="10.1234/test",
        link="https://nature.com/test",
        abstract="Test abstract",
        journal="Nature",
        published_date=datetime.now()
    )
    ranked = rank_papers([paper])
    assert len(ranked) == 1
    assert ranked[0] == paper 