import logging
import webbrowser
from datetime import datetime
import os
from app.fetcher import fetch_today_articles
from app.summarizer import summarize_papers
from app.ranker import rank_papers
from app.renderer import render_digest
from app.github_uploader import push_to_github
from app.config import Config

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main orchestration function."""
    try:
        # Get today's date
        today = datetime.now().strftime('%Y-%m-%d')
        logger.info(f"Starting digest generation for {today}")

        # Fetch articles
        papers = fetch_today_articles()
        if not papers:
            logger.error("No papers fetched, exiting")
            return

        # Generate summaries
        papers = summarize_papers(papers)
        logger.info(f"Generated summaries for {len(papers)} papers")

        # Rank papers
        papers = rank_papers(papers)
        logger.info("Ranked papers based on preferences")

        # Generate HTML
        html = render_digest(today, papers)
        if not html:
            logger.error("Failed to generate HTML")
            return

        # Create digests directory if it doesn't exist
        os.makedirs('digests', exist_ok=True)

        # Save locally
        local_path = f"digests/{today}.html"
        with open(local_path, 'w') as f:
            f.write(html)
        logger.info(f"Saved digest to {local_path}")

        # Push to GitHub
        github_path = Config.DIGEST_PATH_FMT.format(date=today)
        if push_to_github(github_path, html):
            logger.info(f"Successfully pushed to GitHub: {github_path}")
        else:
            logger.error("Failed to push to GitHub")

        # Open in browser
        webbrowser.open(f'file://{os.path.abspath(local_path)}')
        logger.info("Opened digest in browser")

    except Exception as e:
        logger.error(f"Error in main process: {str(e)}")

if __name__ == "__main__":
    main() 