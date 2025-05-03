from flask import Blueprint, request, jsonify
from sqlalchemy import func
from .models import db, Vote, Paper
from .config import Config

bp = Blueprint('feedback', __name__)

@bp.route('/feedback')
def feedback():
    """Handle paper feedback (up/down votes)."""
    try:
        doi = request.args.get('doi')
        vote_type = request.args.get('vote')
        
        if not doi or vote_type not in ('up', 'down'):
            return jsonify({"error": "Invalid parameters"}), 400
        
        # Verify paper exists
        paper = Paper.query.filter_by(doi=doi).first()
        if not paper:
            return jsonify({"error": "Paper not found"}), 404
        
        # Record vote
        vote = Vote(paper_doi=doi, vote=vote_type)
        db.session.add(vote)
        db.session.commit()
        
        return jsonify({"message": "Thank you for your feedback!"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route('/stats')
def stats():
    """Get voting statistics for papers."""
    try:
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
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500 