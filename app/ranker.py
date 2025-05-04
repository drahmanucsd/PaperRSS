import logging
from typing import List, Dict, Tuple
from openai import OpenAI
from app.models import Paper
from app.config import Config
import os

logger = logging.getLogger(__name__)

def load_preferences() -> Dict[str, int]:
    """Load and parse preferences from file."""
    preferences = {}
    try:
        with open(Config.PREFERENCES_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    parts = line.split()
                    if len(parts) >= 2:
                        topic = ' '.join(parts[:-1])
                        try:
                            weight = int(parts[-1])
                            preferences[topic] = weight
                        except ValueError:
                            logger.warning(f"Invalid weight in preferences: {line}")
    except Exception as e:
        logger.error(f"Error loading preferences: {str(e)}")
    return preferences

def rank_papers(papers: List[Paper]) -> List[Paper]:
    """
    Rank papers based on user preferences using OpenAI.
    Returns the papers in ranked order.
    """
    if not papers:
        logger.warning("No papers to rank")
        return papers

    preferences = load_preferences()
    if not preferences:
        logger.warning("No preferences loaded, returning papers in original order")
        return papers

    try:
        # Initialize OpenAI client
        client = OpenAI(api_key=Config.OPENAI_API_KEY)

        # Prepare paper information for ranking
        paper_info = []
        for i, paper in enumerate(papers, 1):
            info = (
                f"{i}. Title: {paper.title}\n"
                f"   DOI: {paper.doi}\n"
                f"   Abstract: {paper.abstract}\n"
                f"   Summary: {paper.summary}\n"
            )
            paper_info.append(info)

            # Create ranking prompt
            prompt = (
                "Here are the user's research interests and their weights (1-10, higher is more important):\n"
                f"{preferences}\n\n"
                "Please rank the following papers by how well they match these interests, "
                "considering both the weights and the content. Return only the numbers in order of relevance:\n\n"
                f"{''.join(paper_info)}"
            )

        # Call OpenAI API
        logger.info("Generating paper rankings")
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "You are a scientific paper ranker. Return only the numbers in order of relevance."},
                {"role": "user", "content": prompt}
            ]
        )

        # Parse rankings from response
        ranked_indices = []
        try:
            # Extract numbers from response
            response_text = response.choices[0].message.content
            ranked_indices = [int(num) for num in response_text.split() if num.isdigit()]
            
            # Validate rankings
            if len(ranked_indices) != len(papers):
                logger.warning("Incomplete rankings received, using original order")
                return papers
                
            # Reorder papers based on rankings
            ranked_papers = [papers[i-1] for i in ranked_indices]
            logger.info("Successfully ranked papers")
            return ranked_papers

        except Exception as e:
            logger.error(f"Error parsing rankings: {str(e)}")
            return papers

    except Exception as e:
        logger.error(f"Error generating rankings: {str(e)}")
        return papers 