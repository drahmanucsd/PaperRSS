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
import glob
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def update_index_html():
    """Update the index.html file with the latest digests."""
    try:
        # Get all digest files sorted by date (newest first)
        digest_files = sorted(glob.glob('digests/*.html'), reverse=True)
        
        # Read the current index.html
        with open('index.html', 'r') as f:
            soup = BeautifulSoup(f.read(), 'html.parser')
        
        # Find the digest list
        digest_list = soup.find('ul', class_='digest-list')
        if not digest_list:
            logger.error("Could not find digest list in index.html")
            return False
        
        # Clear existing items
        digest_list.clear()
        
        # Add new items
        for digest_file in digest_files[:5]:  # Show only the 5 most recent digests
            date_str = os.path.basename(digest_file).replace('.html', '')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d')
                formatted_date = date.strftime('%B %d, %Y')
            except ValueError:
                formatted_date = date_str
            
            li = soup.new_tag('li')
            a = soup.new_tag('a', href=digest_file)
            a.string = f"{formatted_date} Digest"
            li.append(a)
            digest_list.append(li)
        
        # Write the updated index.html
        with open('index.html', 'w') as f:
            f.write(str(soup))
        
        logger.info("Successfully updated index.html with latest digests")
        return True
        
    except Exception as e:
        logger.error(f"Error updating index.html: {str(e)}")
        return False

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

        # Update index.html
        if update_index_html():
            logger.info("Successfully updated index.html")
        else:
            logger.error("Failed to update index.html")

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