import pytest
from datetime import datetime
from unittest.mock import patch, MagicMock
from app.models import Paper
from app.summarizer import summarize_papers

def test_summarize_papers_empty():
    """Test summarizing empty paper list."""
    result = summarize_papers([])
    assert result == []

@patch('app.summarizer.OpenAI')
def test_summarize_papers_success(mock_openai):
    """Test successful paper summarization."""
    # Create test papers
    papers = [
        Paper(
            title="Test Paper 1",
            doi="10.1234/test1",
            link="https://nature.com/test1",
            abstract="Test abstract 1",
            journal="Nature",
            published_date=datetime.now()
        ),
        Paper(
            title="Test Paper 2",
            doi="10.1234/test2",
            link="https://nature.com/test2",
            abstract="Test abstract 2",
            journal="Nature",
            published_date=datetime.now()
        )
    ]
    
    # Mock OpenAI response
    mock_response = MagicMock()
    mock_response.choices = [
        MagicMock(message=MagicMock(content="Summary 1")),
        MagicMock(message=MagicMock(content="Summary 2"))
    ]
    mock_client = MagicMock()
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    
    # Test summarization
    result = summarize_papers(papers)
    
    assert len(result) == 2
    assert result[0].summary == "Summary 1"
    assert result[1].summary == "Summary 2"
    assert mock_client.chat.completions.create.call_count == 1

@patch('app.summarizer.OpenAI')
def test_summarize_papers_api_error(mock_openai):
    """Test handling of API error during summarization."""
    # Create test paper
    paper = Paper(
        title="Test Paper",
        doi="10.1234/test",
        link="https://nature.com/test",
        abstract="Test abstract",
        journal="Nature",
        published_date=datetime.now()
    )
    
    # Mock API error
    mock_client = MagicMock()
    mock_client.chat.completions.create.side_effect = Exception("API Error")
    mock_openai.return_value = mock_client
    
    # Test summarization
    result = summarize_papers([paper])
    
    assert len(result) == 1
    assert result[0].summary == "Summary generation failed." 