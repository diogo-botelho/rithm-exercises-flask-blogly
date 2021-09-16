"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.get("/")
def redirect_to_users():
    """Redirect to Users page"""

    return redirect("/users")

@app.get("/users")
def show_users():
    """Show a list of all users"""

    users = User.query.all() 

    return render_template("users.html", 
                            users = users)

@app.get("/users/new")
def show_new_user_form():
    """Show form new user"""

    return render_template("new-user.html")

@app.post("/users/new")
def add_user():
    """Add new user"""

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    new_user = User(first_name=first_name,last_name=last_name,image_url=image_url)
    
    db.session.add(new_user)
    db.session.commit()
    
    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_details(user_id):
    """Show details for selected user"""

    user = User.query.get(user_id)

    return render_template("/user-detail.html", user=user )

@app.get("/users/<int:user_id>/edit")
def show_user_edit_form(user_id):
    """Show the edit page for a user"""

    user = User.query.get(user_id)

    return render_template("edit-user.html", user=user)

@app.post("/users/<int:user_id>/edit")
def update_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]

    edited_user = User.query.get(user_id)

    edited_user.first_name = first_name
    edited_user.last_name = last_name
    edited_user.image_url = image_url

    db.session.commit()

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get(user_id)
    breakpoint()
    db.session.delete(user)
    breakpoint()
    db.session.commit()
    breakpoint()

    return redirect("/users")

