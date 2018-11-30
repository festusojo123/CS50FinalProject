import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///storage.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # show users who is currently going to an event through a calendar
    # display events near the user on that day (or just in Boston in general)
    # display users who are already at that event
    # put these events on said calendar?
    currentUser = session["user_id"]
    return render_template("index.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    # collect username info
    username = request.args.get("username")
    checker = db.execute("SELECT * FROM users WHERE username = :t", t=username)
    if not len(username) or checker:
        return jsonify(False)
    else:
        return jsonify(True)



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/addevent")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user
    if request.method == "POST":
        # make sure there's a username
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        checker = db.execute("SELECT * FROM users WHERE username = :t", t=username)

        if not username or len(checker):
            return apology("Sorry! Your username has already been registered!")

        # make sure password and verify it
        # require that a user input a password & verify it
        if not password:
            return apology("Sorry! Please input a password and make sure they match!")

        if password != confirmation:
            return apology("Sorry! Please input a password and make sure they match!")

        # insert into users and hashed password
        hashedValue = generate_password_hash(password)
        signedIn = db.execute("INSERT INTO users (username, hash) VALUES(:username, :hash)", username=username, hash=hashedValue)

        session["user_id"] = signedIn

        flash('Registered!')

        return redirect("/")

    # post request now
    if request.method == "GET":
        return render_template("register.html")

@app.route("/addevents", methods=["GET", "POST"])
@login_required
def addevents():
    # allow them to add new events & set them up as event organizer
    # allow them to sign up for event already on calendar
    # email person who's in charge of that event
    currentUser = session["user_id"]
    if request.method == "POST":
        return render_template("addevents.html")
    else:
        return render_template("addevents.html")


@app.route("/venmo", methods=["GET", "POST"])
@login_required
def venmo():
    currentUser = session["user_id"]
    checked = db.execute("SELECT symbol FROM storage WHERE user_id = :t", t=currentUser)
    checker = set(val for dic in checked for val in dic.values())
    for x in checker:
         x

    """Allows user to log in to Venmo to pay any registration fees"""
    if request.method == "GET":
        return render_template("venmo.html", checker=checker)

    if request.method == "POST":
        flash('You have paid the fee for your event!')
        return redirect("/")

@app.route("/transport", methods=["GET", "POST"])
@login_required
def transport():
    """Allow user to log in to their lyft/uber accounts"""
    if request.method == "GET":
        return render_template("transport.html")

    if request.method == "POST":
        flash('Your ride has been ordered through the 3rd party app!')
        return redirect("/")



def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
