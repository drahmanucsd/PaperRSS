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

    # Initialize OpenAI client
    client = OpenAI(api_key=Config.OPENAI_API_KEY)

    # Process each paper individually
    for paper in papers:
        try:
            messages = [
                {"role": "system", "content": "You are a scientific paper summarizer. Provide clear, concise summaries."},
                {
                    "role": "user", 
                    "content": (
                        f"Title: {paper.title}\n"
                        f"Abstract: {paper.abstract}\n\n"
                        "Please provide a concise two-sentence summary focusing on the key findings and novelty. "
                        "First sentence should describe the main discovery, second should highlight its significance."
                    )
                }
            ]

            # Call OpenAI API
            logger.info(f"Generating summary for: {paper.title}")
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages
            )

            # Extract summary from response
            paper.summary = response.choices[0].message.content.strip()
            logger.info(f"Added summary for: {paper.title}")

        except Exception as e:
            logger.error(f"Error generating summary for {paper.title}: {str(e)}")
            paper.summary = "Summary generation failed."

    return papers 