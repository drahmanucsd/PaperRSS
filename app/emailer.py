from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from datetime import datetime
from .config import Config

def build_digest_html(papers, summaries, highlight_title=None, highlight_justification=None):
    """Build HTML content for the email digest."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Nature Digest</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                line-height: 1.6;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            .paper {
                margin-bottom: 30px;
                padding: 15px;
                border: 1px solid #eee;
                border-radius: 5px;
            }
            .title {
                font-size: 1.2em;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .journal {
                color: #666;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .summary {
                margin: 10px 0;
            }
            .feedback {
                margin-top: 10px;
            }
            .feedback a {
                text-decoration: none;
                font-size: 1.2em;
                margin-right: 10px;
                cursor: pointer;
            }
            .feedback a:hover {
                opacity: 0.7;
            }
            .paper-summary {
                margin: 15px 0;
                padding: 10px;
                background: #f9f9f9;
                border-radius: 4px;
            }
            .paper-summary h3 {
                margin: 0 0 10px 0;
                color: #333;
            }
            .paper-summary p {
                margin: 0;
                color: #444;
            }
        </style>
    </head>
    <body>
        <h1>Nature Digest</h1>
        <div class="date">""" + datetime.now().strftime("%Y-%m-%d") + """</div>
    """
    
    # First add the summary section
    html += """
    <div class="summary-section">
        <h2>Today's Highlights</h2>
        <div class="paper-summaries">
    """
    
    # Add each paper's summary
    for paper, summary in zip(papers, summaries.split('<div class="paper-summary">')[1:]):
        html += f"""
        <div class="paper-summary">
            <h3>{paper.title}</h3>
            {summary}
        </div>
        """
    
    html += """
        </div>
    </div>
    <h2>Papers</h2>
    """
    
    # Then add the detailed paper sections
    for paper in papers:
        is_highlight = (paper.title.strip() == (highlight_title or "").strip())
        
        html += f"""
        <div class="paper">
            <div class="title" {'style=\"color: red;\"' if is_highlight else ''}>
                <a href="https://doi.org/10.1038/{paper.doi}" style="text-decoration: none; color: inherit;">{paper.title}</a>
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