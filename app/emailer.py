from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
from .config import Config

def build_digest_html(papers, summaries):
    """Build HTML content for the email digest."""
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
            .paper {{ margin-bottom: 20px; padding: 10px; border-left: 3px solid #007bff; }}
            .title {{ font-weight: bold; color: #007bff; }}
            .journal {{ color: #666; font-style: italic; }}
            .summary {{ margin: 10px 0; }}
            .feedback {{ margin-top: 10px; }}
            .feedback a {{ margin-right: 10px; text-decoration: none; }}
            .paper-summary h3 {{ margin: 0 0 10px 0; }}
            .paper-summary p {{ margin: 0; }}
        </style>
    </head>
    <body>
        <h1>Nature Digest - {datetime.now().strftime('%Y-%m-%d')}</h1>
        {summaries}
        <h2>Papers</h2>
    """
    
    for paper in papers:
        html += f"""
        <div class="paper">
            <div class="title">{paper.title}</div>
            <div class="journal">{paper.journal} (IF: {paper.impact_factor})</div>
            <div class="feedback">
                <a href="https://{Config.API_DOMAIN}/feedback?doi={paper.doi}&vote=up">👍</a>
                <a href="https://{Config.API_DOMAIN}/feedback?doi={paper.doi}&vote=down">👎</a>
            </div>
        </div>
        """
    
    html += """
    </body>
    </html>
    """
    return html

def send_digest(papers, summaries):
    """Send the digest email using SendGrid."""
    if not Config.SENDGRID_API_KEY or not Config.EMAIL_FROM or not Config.EMAIL_RECIPIENTS:
        raise ValueError("Missing email configuration")
    
    html_content = build_digest_html(papers, summaries)
    
    message = Mail(
        from_email=Email(Config.EMAIL_FROM),
        to_emails=[To(email) for email in Config.EMAIL_RECIPIENTS],
        subject=f"Nature Digest - {datetime.now().strftime('%Y-%m-%d')}",
        html_content=Content("text/html", html_content)
    )
    
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        return response.status_code == 202
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False 