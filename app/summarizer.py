import logging
from typing import List
from openai import OpenAI
from app.models import Paper
from app.config import Config
import os

logger = logging.getLogger(__name__)

def summarize_papers(papers: List[Paper]) -> List[Paper]:
    """
    Generate summaries for a list of papers using OpenAI.
    Returns the same list with summaries added.
    """
    if not papers:
        logger.warning("No papers to summarize")
        return papers

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        # Prepare prompts for all papers
        prompts = []
        for paper in papers:
            prompt = (
                f"Title: {paper.title}\n"
                f"Abstract: {paper.abstract}\n\n"
                "Please provide a concise two-sentence summary focusing on the key findings and novelty. "
                "First sentence should describe the main discovery, second should highlight its significance."
            )
            prompts.append(prompt)

        # Call OpenAI API
        logger.info(f"Generating summaries for {len(papers)} papers")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a scientific paper summarizer. Provide clear, concise summaries."},
                *[{"role": "user", "content": prompt} for prompt in prompts]
            ]
        )

        # Extract summaries from response
        summaries = [choice.message.content.strip() for choice in response.choices]
        
        # Add summaries to papers
        for paper, summary in zip(papers, summaries):
            paper.summary = summary
            logger.info(f"Added summary for: {paper.title}")

    except Exception as e:
        logger.error(f"Error generating summaries: {str(e)}")
        # Continue with unsummarized papers rather than failing completely
        for paper in papers:
            if not paper.summary:
                paper.summary = "Summary generation failed."

    return papers 