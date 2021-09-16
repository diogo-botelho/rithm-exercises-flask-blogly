from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    '''Connect to database.'''

    db.app = app
    db.init_app(app)


"""Models for Blogly."""


class User(db.Model):
    '''User.'''

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(30),
                           nullable=False)
    last_name = db.Column(db.String(30),
                          nullable=False)
    image_url = db.Column(db.Text,
                          nullable=True,
                          default="https://anthonycarbonepersonalinjurylawyer.com/wp-content/uploads/2018/06/shutterstock_126920099.jpg")


class Post(db.Model):
    '''Post.'''

    __tablename__ = "posts"

    id = db.Column(db.Integer, 
                    primary_key=True, 
                    autoincrement=True)
    title = db.Column(db.String(100), 
                        nullable=False)
    content = db.Column(db.Text, 
                        nullable=False)
    created_at = db.Column(db.DateTime, 
                            nullable=False,
                            default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"))

    user = db.relationship('User', backref='posts')
