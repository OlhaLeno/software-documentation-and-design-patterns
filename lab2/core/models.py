from flask_sqlalchemy import SQLAlchemy
from datetime import date

db = SQLAlchemy()

class Content(db.Model):
    __tablename__ = 'content'
    
    contentId = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    releaseDate = db.Column(db.Date)
    rating = db.Column(db.Float)
    genre = db.Column(db.String(100))
    director = db.Column(db.String(255))
    
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'content',
        'polymorphic_on': type
    }

class Movie(Content):
    __tablename__ = 'movies'
    
    contentId = db.Column(db.Integer, db.ForeignKey('content.contentId'), primary_key=True)
    duration = db.Column(db.Integer)
    
    __mapper_args__ = {
        'polymorphic_identity': 'movie'
    }

class Serial(Content):
    __tablename__ = 'serials'
    
    contentId = db.Column(db.Integer, db.ForeignKey('content.contentId'), primary_key=True)
    seasonsCount = db.Column(db.Integer)
    episodesCount = db.Column(db.Integer)
    
    seasons = db.relationship('Season', backref='serial', cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'serial'
    }

class Season(db.Model):
    __tablename__ = 'seasons'
    
    seasonId = db.Column(db.Integer, primary_key=True)
    serialId = db.Column(db.Integer, db.ForeignKey('serials.contentId'), nullable=False)
    
    seasonTitle = db.Column(db.String(255))
    seasonNumber = db.Column(db.Integer)
    numberOfEpisodes = db.Column(db.Integer)
    releaseDate = db.Column(db.Date)
    
    episodes = db.relationship('Episode', backref='season', cascade="all, delete-orphan")

class Episode(db.Model):
    __tablename__ = 'episodes'
    
    episodeId = db.Column(db.Integer, primary_key=True)
    seasonId = db.Column(db.Integer, db.ForeignKey('seasons.seasonId'), nullable=False)
    
    episodeTitle = db.Column(db.String(255))
    duration = db.Column(db.Integer)