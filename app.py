import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, Director, Movie, Review, Rating
from config import Config
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)
app.config.from_object(Config)

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to Movie-App API'}), 200


@app.route('/api/directors', methods=['POST'])
def create_director():
    data = request.get_json()
    director = Director(
        name=data['name'],
        age=data.get('age'),
        gender=data.get('gender')
    )
    db.session.add(director)
    db.session.commit()
    return jsonify({'message': 'Director created successfully', 'id': director.id}), 201

@app.route('/api/directors', methods=['GET'])
def get_directors():
    directors = Director.query.all()
    return jsonify([{
        'id': director.id,
        'name': director.name,
        'age': director.age,
        'gender': director.gender
    } for director in directors])


@app.route('/api/movies', methods=['POST'])
def create_movie():
    data = request.get_json()
    movie = Movie(
        title=data['title'],
        director_id=data['director_id']
    )
    db.session.add(movie)
    db.session.commit()
    return jsonify({'message': 'Movie created successfully', 'id': movie.id}), 201

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify([{
        'id': movie.id,
        'title': movie.title,
        'director': movie.director.name
    } for movie in movies])

@app.route('/api/directors/<int:director_id>/movies', methods=['GET'])
def get_director_movies(director_id):
    movies = Movie.query.filter_by(director_id=director_id).all()
    return jsonify([{
        'id': movie.id,
        'title': movie.title
    } for movie in movies])


@app.route('/api/movies/<int:movie_id>/reviews', methods=['POST'])
def create_review(movie_id):
    data = request.get_json()
    
    # Create rating first
    rating = Rating(
        movie_id=movie_id,
        rating=data['rating']
    )
    db.session.add(rating)
    db.session.commit()
    
    # Create review with rating_id
    review = Review(
        movie_id=movie_id,
        rating_id=rating.id,
        review=data['review']
    )
    db.session.add(review)
    db.session.commit()
    
    # Get movie title for response
    movie = Movie.query.get(movie_id)
    
    return jsonify({
        'id': review.id,
        'review': review.review,
        'rating': rating.rating,
        'movie_title': movie.title
    }), 201

@app.route('/api/movies/<int:movie_id>/reviews', methods=['GET'])
def get_movie_reviews(movie_id):
    reviews = Review.query.filter_by(movie_id=movie_id).all()
    movie = Movie.query.get_or_404(movie_id)
    return jsonify([{
        'id': review.id,
        'review': review.review,
        'rating': Rating.query.get(review.rating_id).rating,
        'movie_title': movie.title
    } for review in reviews])

@app.route('/api/reviews/<int:review_id>', methods=['PATCH'])
def update_review(review_id):
    review = Review.query.get_or_404(review_id)
    data = request.get_json()
    
    # Update review text
    if 'review' in data:
        review.review = data['review']
    
    # Update rating if provided
    if 'rating' in data:
        rating = Rating.query.get(review.rating_id)
        if rating:
            rating.rating = data['rating']
    
    db.session.commit()
    
    # Return updated review with movie title
    movie = Movie.query.get(review.movie_id)
    return jsonify({
        'id': review.id,
        'review': review.review,
        'rating': Rating.query.get(review.rating_id).rating,
        'movie_title': movie.title
    }), 200

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    
    rating = Rating.query.get(review.rating_id)
    if rating:
        db.session.delete(rating)
    db.session.delete(review)
    db.session.commit()
    return jsonify({'message': 'Review deleted successfully'})

@app.route('/api/reviews', methods=['GET'])
def get_all_reviews():
    reviews = Review.query.all()
    return jsonify([{
        'id': review.id,
        'movie_id': review.movie_id,
        'rating_id': review.rating_id,
        'review': review.review
    } for review in reviews])

@app.route('/api/ratings', methods=['GET'])
def get_all_ratings():
    ratings = Rating.query.all()
    return jsonify([{
        'id': rating.id,
        'movie_id': rating.movie_id,
        'rating': rating.rating
    } for rating in ratings])

@app.route('/api/directors/<int:director_id>', methods=['DELETE'])
def delete_director(director_id):
    director = Director.query.get_or_404(director_id)
    db.session.delete(director)
    db.session.commit()
    return jsonify({'message': 'Director deleted successfully'}), 200

@app.route('/api/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    return jsonify({'message': 'Movie deleted successfully'}), 200

@app.route('/api/directors/<int:director_id>', methods=['PATCH'])
def update_director(director_id):
    director = Director.query.get_or_404(director_id)
    data = request.get_json()
    
    director.name = data.get('name', director.name)
    director.age = data.get('age', director.age)
    director.gender = data.get('gender', director.gender)
    
    db.session.commit()
    
    return jsonify({
        'id': director.id,
        'name': director.name,
        'age': director.age,
        'gender': director.gender
    }), 200

@app.route('/api/movies/<int:movie_id>', methods=['PATCH'])
def update_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    data = request.get_json()
    
    movie.title = data.get('title', movie.title)
    if 'director_id' in data:
        # Verify that the director exists
        director = Director.query.get_or_404(data['director_id'])
        movie.director_id = data['director_id']
    
    db.session.commit()
    
    return jsonify({
        'id': movie.id,
        'title': movie.title,
        'director_id': movie.director_id,
        'director': Director.query.get(movie.director_id).name
    }), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400

@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Internal server error'}), 500


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
