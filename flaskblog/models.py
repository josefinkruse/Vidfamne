from dataclasses import dataclass
from datetime import datetime
from flaskblog import db, login_manager
from flask_login import UserMixin
from sqlalchemy.orm import relationship


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@dataclass
class User(db.Model, UserMixin):
    id: int
    username: str

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    profile_pic = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    pictures = db.relationship('Picture', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.profile_pic}')"


@dataclass
class Folder(db.Model):
    id: int
    title: str
    start_date: datetime
    end_date: datetime
    destinations: str
    description: str
    folder_image: str

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False, default=None)
    end_date = db.Column(db.Date, nullable=False, default=None)
    destinations = db.Column(db.Text)
    description = db.Column(db.Text)  # Vill vi ha vilka som var med på resan?
    folder_image = db.Column(db.String(20), nullable=False, default='default.jpg')

    def __repr__(self):
        return f"Folder('{self.title}', '{self.start_date}', '{self.end_date}', '{self.destinations}', '{self.description}', '{self.folder_image}')"

    # but with the serialize() allows you to get information from relationships
    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'start_date': self.start_date,
            'end_date': self.end_date,
            'destinations': self.destinations,
            'description': self.description,
            'folder_image': self.folder_image
        }


@dataclass # using dataclass you don't need to have the serialize function
class Picture(db.Model):
    # but you need to identify the types of the fields
    id: int
    image_file: str
    date_taken: datetime
    description: str
    place_taken: str
    user: User
    folder: Folder

    id = db.Column(db.Integer, primary_key=True)
    image_file = db.Column(db.String(20), nullable=False)
    date_taken = db.Column(db.DateTime, nullable=False, default=None) #, default=datetime.utcnow)  # Where to get the info?
    description = db.Column(db.Text)
    place_taken = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    folder_id = db.Column(db.Integer, db.ForeignKey('folder.id'), nullable=False)
    folder = relationship(Folder)

    def __repr__(self):
        return f"Picture('{self.image_file}', '{self.date_taken}', '{self.description}', " \
               f"'{self.place_taken}', '{self.user}', '{self.folder}')"

    # but with the serialize() allows you to get information from relationships
    @property
    def serialize(self):
        return {
            'id': self.id,
            'date_taken': self.date_taken,
            'image_file': self.image_file,
            'description': self.description,
            'place_taken': self.place_taken,
            'user': self.user_id,
            'username': self.user.username,
            'folder_id': self.folder_id,    #changed...
            'folder_title': self.folder.title    #changed...
        }


@dataclass
class Comment(db.Model):
    id: int
    content: str
    user: User

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = relationship(User)
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'), nullable=False)
    picture = relationship(Picture)


@dataclass
class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_expired = db.Column(db.DateTime, nullable=False)
    token = db.Column(db.String(60), nullable=False, index=True) # index helps searching