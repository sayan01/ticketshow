from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from app import app
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app, db)

# Creating Model
show_genre_table = db.Table('show_genre',
    db.Column('show_id', db.Integer, db.ForeignKey('show.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'{self.username}'
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    
class Venue(db.Model):
    __tablename__ = 'venue'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    shows = db.relationship('Show', backref='venue', lazy=True)
    

class Show(db.Model):
    __tablename__ = 'show'
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)
    name = db.Column(db.String(128), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    timing = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    genres = db.relationship('Genre', secondary=show_genre_table, backref='shows', lazy=True)
    __table_args__ = (db.UniqueConstraint('venue_id', 'timing'),)

class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()
