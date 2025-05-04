import logging
from datetime import datetime
from typing import List
import jinja2
import os
from app.models import Paper
from app.config import Config

logger = logging.getLogger(__name__)

def render_digest(date: str, papers: List[Paper]) -> str:
    """
    Generate HTML for the digest.
    Returns the HTML content as a string.
    """
    if not papers:
        logger.warning("No papers to render")
        return ""

    # Create template directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(template_dir, exist_ok=True)

    # Create template file
    template_path = os.path.join(template_dir, 'digest.html')
    if not os.path.exists(template_path):
        with open(template_path, 'w') as f:
            f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ date }} Nature Digest</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #eee;
            padding-bottom: 10px;
        }
        .paper {
            margin-bottom: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        .paper h2 {
            margin-top: 0;
            color: #2c3e50;
        }
        .paper a {
            color: #3498db;
            text-decoration: none;
        }
        .paper a:hover {
            text-decoration: underline;
        }
        .doi {
            color: #666;
            font-size: 0.9em;
        }
        .summary {
            margin-top: 10px;
            color: #444;
        }
        .journal {
            color: #666;
            font-style: italic;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <h1>{{ date }} Nature Digest</h1>
    {% for paper in papers %}
    <div class="paper">
        <h2><a href="{{ paper.link }}">{{ paper.title }}</a></h2>
        <div class="journal">{{ paper.journal }}</div>
        <div class="doi">DOI: {{ paper.doi }}</div>
        <div class="summary">{{ paper.summary }}</div>
    </div>
    {% endfor %}
</body>
</html>""")

    # Load and render template
    try:
        env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))
        template = env.get_template('digest.html')
        html = template.render(date=date, papers=papers)
        logger.info(f"Generated HTML digest for {date}")
        return html
    except Exception as e:
        logger.error(f"Error rendering digest: {str(e)}")
        return "" 