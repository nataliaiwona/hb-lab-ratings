"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, jsonify, render_template, redirect, request, flash, 
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy import func

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
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/register', methods=["GET"])
def register_form():
    """Display user registration form."""

    return render_template("register_form.html")


@app.route('/register', methods=["POST"])
def register_process():
    """Process registration form."""

    username = request.form.get("username")
    password = request.form.get("password")

    email_search = User.query.filter_by(email = username).all()

    if email_search == []: # not in database
        user = User(email=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!")
        return redirect("/")
    else:
        flash("Email already exists. Try again.")
        # return render_template("register_form.html")
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
        session["login"] = User.query.filter_by
        flash("Logged in!")
        return redirect("/")












if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000)
