import logging
import os
from github import Github
from app.config import Config

logger = logging.getLogger(__name__)

def push_to_github(path: str, content: str) -> bool:
    """
    Push content to GitHub repository.
    Returns True if successful, False otherwise.
    """
    try:
        # Initialize GitHub client
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            logger.error("GitHub token not found in environment variables")
            return False

        gh = Github(github_token)
        repo = gh.get_repo(Config.GITHUB_REPO)

        # Check if file exists
        try:
            contents = repo.get_contents(path, ref=Config.GITHUB_BRANCH)
            # Update existing file
            repo.update_file(
                path=path,
                message=f"Update digest {path}",
                content=content,
                sha=contents.sha,
                branch=Config.GITHUB_BRANCH
            )
            logger.info(f"Updated existing file: {path}")
        except Exception:
            # Create new file
            repo.create_file(
                path=path,
                message=f"Add digest {path}",
                content=content,
                branch=Config.GITHUB_BRANCH
            )
            logger.info(f"Created new file: {path}")

        return True

    except Exception as e:
        logger.error(f"Error pushing to GitHub: {str(e)}")
        return False 