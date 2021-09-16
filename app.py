"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post
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
    image_url = request.form["image-url"] or None #Code review: Without the "or None" it was passing an empty string and the model needs a Null to put the template image

    new_user = User(
                    first_name=first_name,
                    last_name=last_name,
                    image_url=image_url
                    )
    
    db.session.add(new_user)
    db.session.commit()

    flash(f"User {first_name} {last_name} successfully added.")
    
    return redirect("/users")

@app.get("/users/<int:user_id>")
def show_user_details(user_id):
    """Show details for selected user"""

    user = User.query.get_or_404(user_id) #Code Review: .get returns the page with all the values as "None" but still showing the template HTML. Also one click away from a bug if users try to delete the non-existing user

    posts = user.posts

    return render_template(
                            "/user-detail.html",
                            user= user,
                            posts= posts)

@app.get("/users/<int:user_id>/edit")
def show_user_edit_form(user_id):
    """Show the edit page for a user"""

    user = User.query.get(user_id)

    return render_template("edit-user.html", user=user)

@app.post("/users/<int:user_id>/edit")
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""

    edited_user = User.query.get_or_404(user_id) #Code Review

    edited_user.first_name = request.form["first-name"]
    edited_user.last_name = request.form["last-name"]
    edited_user.image_url = request.form["image-url"]

    db.session.commit()

    flash("User details successfully edited.")

    return redirect("/users")

@app.post("/users/<int:user_id>/delete")
def delete_user(user_id):
    """Delete the user."""

    user = User.query.get(user_id)
    db.session.delete(user) #user.query.get.delete also a good alternative
    db.session.commit()

    flash("User successfully deleted.")

    return redirect("/users")

@app.get("/users/<int:user_id>/posts/new")
def show_add_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    return render_template("new-post.html", user=user)

@app.post("/users/<int:user_id>/posts/new")
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""

    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    flash(f"'{new_post.title}' was successfully added.")
    
    return redirect(f"/users/{user_id}")

@app.get("/posts/<int:post_id>")
def show_post(post_id):
    """Show post."""

    post = Post.query.get_or_404(post_id)
    
    user = post.user

    return render_template(
                            "post-detail.html",
                            post = post,
                            user = user
                            )

@app.get("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """Show form to edit post."""

    post = Post.query.get_or_404(post_id)

    user = post.user

    return render_template(
                            "edit-post.html",
                            post = post,
                            user = user
                            )

@app.post("/posts/<int:post_id>/edit")
def edit_post(post_id):
    """Edit post."""

    edited_post = Post.query.get_or_404(post_id) #Code Review

    edited_post.title = request.form["title"]
    edited_post.content = request.form["content"]

    db.session.commit()

    flash("Post successfully edited.")

    return redirect(f"/posts/{post_id}")

@app.post("/posts/<int:post_id>/delete")
def delete_post(post_id):
    """Delete post."""

    post = Post.query.get(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()

    flash("Post successfully deleted.")

    return redirect(f"/users/{user.id}")