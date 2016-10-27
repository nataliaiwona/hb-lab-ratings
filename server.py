"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, 
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy import func

from datetime import datetime

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "randomKeyGenerated1837492RandomKeyGeneratedLadidadidah00!!"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    a = jsonify([1,3])
    
    return render_template("homepage.html")


@app.route('/users')
def user_list():
    """Show entire list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/users/<user_id>')
def user_info(user_id):
    """Specific user info (age, zipcode, list of movies rated and scores)."""

    user = User.query.filter_by(user_id=user_id).first()
    age = user.age
    zipcode = user.zipcode
    ratings = user.ratings

    return render_template("user_details.html", age=age,
                                                zipcode=zipcode,
                                                ratings=ratings,
                                                user_id=user_id)


@app.route('/register', methods=["GET"])
def register_form():
    """Display user registration form."""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Process registration form."""

    username = request.form.get("username")
    password = request.form.get("password")

    email_search = User.query.filter_by(email=username).all()

    if email_search == []: # not in database
        user = User(email=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        return redirect("/")
    else:
        flash("Email already exists. Try again.")
        return redirect("/register")


@app.route('/login')
def login_form():
    """Login form."""

    return render_template("login.html")


@app.route('/login', methods=["POST"])
def login_process():
    """Verify login credentials."""

    username = request.form.get("username")
    password = request.form.get("password")

    verify_user = User.query.filter_by(email=username, password=password).all()

    if verify_user == []: # email/password combo is not in database
        flash("The email / password combo provided doesn't match our records.")
        return redirect("/register")
    else:
        user = User.query.filter_by(email=username).first()
        session["login"] = user.user_id
        flash("Logged in!")
        return redirect("/")


@app.route('/logout')
def logout():
    """Logout user."""

    del session["login"]
    flash("You have been logged out.")
    return redirect("/")

# Later...if login in session, display this button
# If login is empty list, might give an error
# Deleting makes it cleaner


@app.route('/movies')
def movie_list():
    """Show entire list of movies."""

    movies = Movie.query.order_by(Movie.title).all()

    return render_template("movie_list.html", movies=movies)


@app.route('/movies/<movie_id>')
def movie_info(movie_id):
    """Specific details about movie."""

    movie = Movie.query.filter_by(movie_id=movie_id).first()
    title = movie.title
    released_at = movie.released_at.strftime('%B %d, %Y')
    imdb_url = movie.imdb_url
    ratings = movie.ratings

    user_id = 0
    user_score = 0
    update_rating = False
    rating = False

    if session.get("login"):
        rating_exists = Rating.query.filter_by(user_id=session['login'], 
                                               movie_id=movie_id).first()
        user_id = session['login']
        if rating_exists: # yep, they rated the movie
            user_score = rating_exists.score
            update_rating = True # give option to update
        else: # they didn't rate movie; give option to rate
            rating = True 
    # pass a variable to jinja that says, "yeah, let them rate"
    return render_template("movie_details.html", title=title,
                                                 released_at=released_at,
                                                 imdb_url=imdb_url,
                                                 ratings=ratings,
                                                 movie_id=movie_id,
                                                 user_score=user_score,
                                                 update_rating=update_rating,
                                                 rating=rating,
                                                 user_id=user_id,)


@app.route('/rate_movie', methods=["POST"])
def rate_movie():
    """Display movie rating form."""

    # updates the database with new movie rating for user

    update_rating = request.form.get("update_rating")
    rating = request.form.get("rating") 
    user_id = request.form.get("user_id")
    movie_id = request.form.get("movie_id")

    if update_rating:
        current_rating = Rating.query.filter_by(movie_id=movie_id, 
                                        user_id=user_id).first()
        current_rating.score = update_rating
        db.session.add(current_rating)
        db.session.commit()
        score = update_rating

    if rating:
        rate = Rating(movie_id=movie_id, user_id=user_id, score=rating)
        db.session.add(rate)
        db.session.commit()
        score = rating

    return jsonify(score)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
