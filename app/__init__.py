from flask import Flask, render_template, send_from_directory, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from .config import Config
from datetime import datetime
import os

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__, 
                static_folder='static',
                static_url_path='/static')
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["https://127.0.0.1:5001", "https://localhost:5001"],
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Accept"]
        }
    })
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Import models to ensure they are registered with SQLAlchemy
    from .models import Paper, Digest, Vote
    
    from .feedback import bp as feedback_bp
    app.register_blueprint(feedback_bp)
    
    @app.route('/votes')
    def show_votes():
        """Show all votes in the database."""
        votes = Vote.query.all()
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Votes</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                tr:nth-child(even) { background-color: #f9f9f9; }
            </style>
        </head>
        <body>
            <h1>Votes</h1>
            <table>
                <tr>
                    <th>ID</th>
                    <th>Paper DOI</th>
                    <th>Vote</th>
                    <th>Timestamp</th>
                    <th>Used for Preferences</th>
                </tr>
        """
        
        for vote in votes:
            html += f"""
                <tr>
                    <td>{vote.id}</td>
                    <td>{vote.paper_doi}</td>
                    <td>{vote.vote}</td>
                    <td>{vote.timestamp}</td>
                    <td>{vote.used_for_prefs}</td>
                </tr>
            """
        
        html += """
            </table>
        </body>
        </html>
        """
        return html
    
    @app.route('/')
    def index():
        """Serve the latest digest."""
        # Get the latest digest
        latest_digest = Digest.query.order_by(Digest.date.desc()).first()
        if not latest_digest:
            return "No digests available yet.", 404
            
        # Get the papers for this digest
        papers = latest_digest.papers
        
        # Build the HTML content
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
            </style>
            <script src="/static/js/feedback.js"></script>
        </head>
        <body>
            <h1>Nature Digest</h1>
            <div class="date">""" + latest_digest.date.strftime("%Y-%m-%d") + """</div>
        """
        
        for paper in papers:
            html += f"""
            <div class="paper">
                <div class="title">
                    <a href="https://doi.org/10.1038/{paper.doi}" style="text-decoration: none; color: inherit;">{paper.title}</a>
                </div>
                <div class="journal">{paper.journal} (IF: {paper.impact_factor})</div>
                <div class="summary">{paper.abstract}</div>
                <div class="feedback">
                    <a href="/feedback?doi={paper.doi}&vote=up">👍</a>
                    <a href="/feedback?doi={paper.doi}&vote=down">👎</a>
                </div>
            </div>
            """
        
        html += """
        </body>
        </html>
        """
        return html
    
    return app 