from flask import Blueprint, request, redirect, jsonify
from sqlalchemy import func
from .models import db, Vote, Paper
from .config import Config

bp = Blueprint('feedback', __name__)

@bp.route('/feedback')
def feedback():
    """Handle paper feedback (up/down votes)."""
    doi = request.args.get('doi')
    vote_type = request.args.get('vote')
    next_url = request.args.get('next')
    
    if not doi or vote_type not in ('up', 'down'):
        return "Invalid parameters", 400
    
    # Verify paper exists
    paper = Paper.query.filter_by(doi=doi).first()
    if not paper:
        return "Paper not found", 404
    
    # Record vote
    vote = Vote(paper_doi=doi, vote=vote_type)
    db.session.add(vote)
    db.session.commit()
    
    # Redirect to paper or next URL
    if next_url:
        return redirect(next_url)
    return redirect(f"https://doi.org/{doi}")

@bp.route('/stats')
def stats():
    """Get voting statistics for papers."""
    stats = db.session.query(
        Vote.paper_doi,
        Vote.vote,
        func.count(Vote.id)
    ).group_by(
        Vote.paper_doi,
        Vote.vote
    ).all()
    
    # Format stats as {doi: {up: count, down: count}}
    result = {}
    for doi, vote_type, count in stats:
        if doi not in result:
            result[doi] = {'up': 0, 'down': 0}
        result[doi][vote_type] = count
    
    return jsonify(result) 