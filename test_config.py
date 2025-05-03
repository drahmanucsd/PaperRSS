import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from github import Github
import sys

def test_sendgrid_config():
    """Test SendGrid configuration and connectivity."""
    load_dotenv()
    
    # Check if environment variables exist
    api_key = os.getenv('SENDGRID_API_KEY')
    email_from = os.getenv('EMAIL_FROM')
    email_recipients = os.getenv('EMAIL_RECIPIENTS')
    
    print("\n=== SendGrid Configuration Test ===")
    print(f"API Key present: {'Yes' if api_key else 'No'}")
    print(f"From Email present: {'Yes' if email_from else 'No'}")
    print(f"Recipients present: {'Yes' if email_recipients else 'No'}")
    
    if not all([api_key, email_from, email_recipients]):
        print("❌ Missing required SendGrid configuration")
        return False
    
    # Test SendGrid connectivity
    try:
        sg = SendGridAPIClient(api_key)
        # Try to get account information to verify API key
        response = sg.client.api_keys.get()
        print("✅ SendGrid API key is valid")
        return True
    except Exception as e:
        print(f"❌ SendGrid API Error: {str(e)}")
        return False

def test_github_config():
    """Test GitHub configuration and connectivity."""
    load_dotenv()
    
    # Check if environment variables exist
    token = os.getenv('GITHUB_TOKEN')
    repo = os.getenv('GITHUB_REPO')
    
    print("\n=== GitHub Configuration Test ===")
    print(f"Token present: {'Yes' if token else 'No'}")
    print(f"Repository specified: {'Yes' if repo else 'No'}")
    
    if not all([token, repo]):
        print("❌ Missing required GitHub configuration")
        return False
    
    # Test GitHub connectivity
    try:
        gh = Github(token)
        # Try to get repository information
        repo_obj = gh.get_repo(repo)
        print(f"✅ Successfully connected to repository: {repo}")
        print(f"Repository visibility: {repo_obj.visibility}")
        return True
    except Exception as e:
        print(f"❌ GitHub API Error: {str(e)}")
        return False

def main():
    """Run all configuration tests."""
    print("Starting configuration tests...")
    
    sendgrid_ok = test_sendgrid_config()
    github_ok = test_github_config()
    
    print("\n=== Test Summary ===")
    print(f"SendGrid Configuration: {'✅ OK' if sendgrid_ok else '❌ Failed'}")
    print(f"GitHub Configuration: {'✅ OK' if github_ok else '❌ Failed'}")
    
    if not all([sendgrid_ok, github_ok]):
        sys.exit(1)

if __name__ == '__main__':
    main() 