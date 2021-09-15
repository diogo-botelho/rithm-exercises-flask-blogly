from flask_sqlalchemy import SQLAlchemy

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


