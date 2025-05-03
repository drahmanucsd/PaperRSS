from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
from .config import Config

def build_digest_html(papers, summaries, highlight_title=None, highlight_justification=None):
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
        </style>
    </head>
    <body>
        <h1>Nature Digest - {datetime.now().strftime('%Y-%m-%d')}</h1>
        <div class="summaries">
            {summaries}
        </div>
        <h2>Papers</h2>
    """
    
    for paper in papers:
        is_highlight = (paper.title.strip() == (highlight_title or "").strip())
        html += f"""
        <div class="paper">
            <div class="title" {'style=\"color: red;\"' if is_highlight else ''}>
                {paper.title}
                {'<span style=\"background: gold; color: #b00; border-radius: 4px; padding: 2px 6px; margin-left: 8px; font-weight: bold; font-size: 0.9em;\">Highlighted</span>' if is_highlight else ''}
            </div>
            <div class="journal">{paper.journal} (IF: {paper.impact_factor})</div>
            {'<div class=\"highlight-justification\" style=\"font-style:italic; color:#b00;\">'+highlight_justification+'</div>' if is_highlight and highlight_justification else ''}
            <div class="summary">{paper.abstract}</div>
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

def send_digest(papers, summaries, highlight_title=None, highlight_justification=None):
    """Send the digest email using SendGrid."""
    if not Config.SENDGRID_API_KEY or not Config.EMAIL_FROM or not Config.EMAIL_RECIPIENTS:
        raise ValueError("Missing email configuration")
    
    html_content = build_digest_html(papers, summaries, highlight_title, highlight_justification)
    
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