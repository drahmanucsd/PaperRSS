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

    # Process papers in batches to avoid token limits
    batch_size = 5
    for i in range(0, len(papers), batch_size):
        batch = papers[i:i + batch_size]
        
        try:
            # Prepare messages for all papers in the batch
            messages = [
                {"role": "system", "content": "You are a scientific paper summarizer. Provide clear, concise summaries."}
            ]
            
            # Add each paper's content to the messages
            for paper in batch:
                messages.append({
                    "role": "user", 
                    "content": (
                        f"Title: {paper.title}\n"
                        f"Abstract: {paper.abstract}\n\n"
                        "Please provide a concise two-sentence summary focusing on the key findings and novelty. "
                        "First sentence should describe the main discovery, second should highlight its significance."
                    )
                })

            # Call OpenAI API for the entire batch
            logger.info(f"Generating summaries for batch of {len(batch)} papers")
            response = client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=messages
            )

            # Extract summaries from response and assign to papers
            summaries = response.choices[0].message.content.strip().split('\n\n')
            for paper, summary in zip(batch, summaries):
                paper.summary = summary.strip()
                logger.info(f"Added summary for: {paper.title}")

        except Exception as e:
            logger.error(f"Error generating summaries for batch: {str(e)}")
            # Mark all remaining papers in this batch as failed
            for p in batch:
                if not p.summary:
                    p.summary = "Summary generation failed."

    return papers 