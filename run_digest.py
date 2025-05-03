from app import create_app, db
from app.models import Paper, Digest, Vote
from app.rss import fetch_all_journals
from app.summary import summarize_abstracts
from app.emailer import send_digest
from app.archiver import commit_digest
from datetime import datetime, timedelta, UTC
import os

def run_digest():
    """Run the complete digest pipeline."""
    app = create_app()
    
    with app.app_context():
        # 1. Fetch new papers
        print("Fetching papers...")
        papers = fetch_all_journals()
        
        if not papers:
            print("No papers found")
            return
        
        # 2. Get papers from last 24 hours
        cutoff = datetime.now(UTC) - timedelta(days=1)
        print(f"Filtering papers published after {cutoff}")
        recent_papers = []
        for paper in papers:
            pub_date = paper.pub_date
            if pub_date.tzinfo is None:
                pub_date = pub_date.replace(tzinfo=UTC)
            if pub_date >= cutoff:
                recent_papers.append(paper)
                print(f"Including paper: {paper.title} (published {pub_date})")
        
        if not recent_papers:
            print("No papers from last 24 hours")
            return
        
        # 3. Sort by impact factor
        sorted_papers = sorted(recent_papers, key=lambda x: x.impact_factor, reverse=True)
        top_papers = sorted_papers[:5]  # Get top 5 papers
        
        # 4. Generate summaries
        print("Generating summaries...")
        abstracts = [p.abstract for p in top_papers]
        summaries = summarize_abstracts(abstracts)
        
        # 5. Send email
        print("Sending email...")
        email_sent = send_digest(top_papers, summaries)
        
        if email_sent:
            # 6. Archive to GitHub
            print("Archiving to GitHub...")
            html_content = f"""
            <html>
            <head>
                <title>Nature Digest - {datetime.now().strftime('%Y-%m-%d')}</title>
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
                {''.join(f'''
                <div class="paper">
                    <div class="title">{p.title}</div>
                    <div class="journal">{p.journal} (IF: {p.impact_factor})</div>
                    <div class="summary">{p.abstract}</div>
                    <div class="feedback">
                        <a href="https://{os.getenv('API_DOMAIN')}/feedback?doi={p.doi}&vote=up">👍</a>
                        <a href="https://{os.getenv('API_DOMAIN')}/feedback?doi={p.doi}&vote=down">👎</a>
                    </div>
                </div>
                ''' for p in top_papers)}
            </body>
            </html>
            """
            commit_digest(html_content)
            
            # 7. Create digest record
            current_date = datetime.now().date()
            
            # Delete existing digest for today if it exists
            existing_digest = Digest.query.filter_by(date=current_date).first()
            if existing_digest:
                print(f"Deleting existing digest for {current_date}")
                db.session.delete(existing_digest)
                db.session.commit()
            
            # Create new digest
            print(f"Creating new digest for {current_date}")
            digest = Digest(date=current_date)
            digest.papers = top_papers
            db.session.add(digest)
            db.session.commit()
            
            print("Digest completed successfully!")
        else:
            print("Failed to send email")

if __name__ == '__main__':
    run_digest() 