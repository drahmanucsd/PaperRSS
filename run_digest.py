from app import create_app, db
from app.models import Paper, Digest, Vote
from app.rss import fetch_all_journals
from app.summary import summarize_abstracts
from app.emailer import send_digest
from app.archiver import commit_digest
from app.preferences import extract_user_preferences, get_user_preferences
from app.highlight import select_highlighted_paper
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
        cutoff = datetime.now(UTC) - timedelta(days=100)
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
        
        # 3. Group papers by journal and select top papers from each
        papers_by_journal = {}
        for paper in recent_papers:
            if paper.journal not in papers_by_journal:
                papers_by_journal[paper.journal] = []
            papers_by_journal[paper.journal].append(paper)
        
        # Sort papers within each journal by impact factor
        for journal in papers_by_journal:
            papers_by_journal[journal].sort(key=lambda x: x.impact_factor, reverse=True)
        
        # Select top papers from each journal
        top_papers = []
        max_papers_per_journal = 2  # Maximum number of papers to select from each journal
        for journal in papers_by_journal:
            top_papers.extend(papers_by_journal[journal][:max_papers_per_journal])
        
        # Sort all selected papers by impact factor
        top_papers.sort(key=lambda x: x.impact_factor, reverse=True)
        top_papers = top_papers[:5]  # Get final top 5 papers
        
        # 4. Generate summaries
        print("Generating summaries...")
        abstracts = [p.abstract for p in top_papers]
        summaries = summarize_abstracts(abstracts)
        
        # 5. Update user preferences and select highlight
        print("Updating user preferences...")
        extract_user_preferences()
        user_prefs = get_user_preferences()
        highlight_title, highlight_justification = select_highlighted_paper(top_papers, user_prefs)
        
        # 6. Send email
        print("Sending email...")
        email_sent = send_digest(top_papers, summaries, highlight_title=highlight_title, highlight_justification=highlight_justification)
        
        if email_sent:
            # 7. Archive to GitHub
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
                    <div class="title" {'style=\"color: red;\"' if p.title.strip() == (highlight_title or "").strip() else ''}>
                        <a href="https://doi.org/10.1038/{p.doi}" style="text-decoration: none; color: inherit;">{p.title}</a>
                        {'<span style=\"background: gold; color: #b00; border-radius: 4px; padding: 2px 6px; margin-left: 8px; font-weight: bold; font-size: 0.9em;\">Highlighted</span>' if p.title.strip() == (highlight_title or "").strip() else ''}
                    </div>
                    <div class="journal">{p.journal} (IF: {p.impact_factor})</div>
                    {'<div class=\"highlight-justification\" style=\"font-style:italic; color:#b00;\">'+highlight_justification+'</div>' if p.title.strip() == (highlight_title or "").strip() and highlight_justification else ''}
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
            
            # 8. Create digest record
            current_date = datetime.now().date()
            
            # Delete existing digest for today if it exists
            existing_digest = Digest.query.filter_by(date=current_date).first()
            if existing_digest:
                db.session.delete(existing_digest)
                db.session.commit()  # Commit the deletion first
            
            # Create new digest
            new_digest = Digest(date=current_date)
            for paper in top_papers:
                new_digest.papers.append(paper)
            db.session.add(new_digest)
            db.session.commit()
            print("Digest record created successfully")
        else:
            print("Failed to send email")

if __name__ == '__main__':
    run_digest() 