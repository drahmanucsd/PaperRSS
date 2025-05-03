from github import Github
from datetime import datetime
import os
from .config import Config

def commit_digest(html_content):
    """Commit the digest to GitHub repository."""
    if not Config.GITHUB_TOKEN or not Config.GITHUB_REPO:
        raise ValueError("Missing GitHub configuration")
    
    try:
        # Initialize GitHub client
        gh = Github(Config.GITHUB_TOKEN)
        repo = gh.get_repo(Config.GITHUB_REPO)
        
        # Prepare file path and content
        date_str = datetime.now().strftime('%Y-%m-%d')
        path = f"digests/{date_str}.html"
        commit_message = f"Add digest for {date_str}"
        
        # Create or update file
        try:
            # Try to get existing file
            contents = repo.get_contents(path)
            repo.update_file(
                path=path,
                message=commit_message,
                content=html_content,
                sha=contents.sha
            )
        except Exception:
            # File doesn't exist, create it
            repo.create_file(
                path=path,
                message=commit_message,
                content=html_content
            )
        
        return True
    except Exception as e:
        print(f"Error committing to GitHub: {str(e)}")
        return False 