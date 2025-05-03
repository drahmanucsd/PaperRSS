from datetime import datetime, UTC
from . import db

class Paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(500), nullable=False)
    journal = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(500), nullable=False)
    abstract = db.Column(db.Text)
    impact_factor = db.Column(db.Float)
    pub_date = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<Paper {self.doi}>'

class Digest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, unique=True, nullable=False)
    papers = db.relationship('Paper', secondary='digest_papers')
    
    def __repr__(self):
        return f'<Digest {self.date}>'

# Association table for many-to-many relationship between Digest and Paper
digest_papers = db.Table('digest_papers',
    db.Column('digest_id', db.Integer, db.ForeignKey('digest.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('paper.id'), primary_key=True)
)

class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paper_doi = db.Column(db.String(100), db.ForeignKey('paper.doi'), nullable=False)
    vote = db.Column(db.String(4), nullable=False)  # 'up' or 'down'
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(UTC))
    
    def __repr__(self):
        return f'<Vote {self.paper_doi} {self.vote}>' 