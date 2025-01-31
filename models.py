from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Director(db.Model):
    __tablename__ = 'directors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(50))
    movies = db.relationship('Movie', backref='director', lazy=True)

class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey('directors.id'), nullable=False)
    reviews = db.relationship('Review', backref='movie', lazy=True)
    ratings = db.relationship('Rating', backref='movie', lazy=True)

class Rating(db.Model):
    __tablename__ = 'rating'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)
    rating_id = db.Column(db.Integer, db.ForeignKey('rating.id'), nullable=False)
    review = db.Column(db.String(500)) 