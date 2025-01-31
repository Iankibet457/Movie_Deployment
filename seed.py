from app import app, db
from models import Director, Movie, Rating, Review
from datetime import datetime

def seed_database():
    with app.app_context():
        
        db.drop_all()
        db.create_all()

        
        director1 = Director(
            name="Christopher Nolan",
            age=52,
            gender="Male"
        )
        director2 = Director(
            name="Martin Scorsese",
            age=81,
            gender="Male"
        )
        
        db.session.add_all([director1, director2])
        db.session.commit()

        
        movie1 = Movie(
            title="Inception",
            director_id=director1.id
        )
        movie2 = Movie(
            title="The Departed",
            director_id=director2.id
        )
        
        db.session.add_all([movie1, movie2])
        db.session.commit()

    
        rating1 = Rating(
            movie_id=movie1.id,
            rating=5
        )
        rating2 = Rating(
            movie_id=movie2.id,
            rating=5
        )
        
        db.session.add_all([rating1, rating2])
        db.session.commit()

        
        review1 = Review(
            movie_id=movie1.id,
            rating_id=rating1.id,
            review="A masterpiece of modern cinema"
        )
        review2 = Review(
            movie_id=movie2.id,
            rating_id=rating2.id,
            review="Brilliant performances all around"
        )
        
        db.session.add_all([review1, review2])
        db.session.commit()

if __name__ == "__main__":
    seed_database()
    print("Database seeded successfully!")