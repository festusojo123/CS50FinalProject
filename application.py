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







    # """Show portfolio of stocks"""
    currentUser = session["user_id"]
    return render_template("index.html")

    # if request.method == "GET":
    #     # select info for each stock and sum the # in each group
    #     stocks = db.execute("SELECT symbol FROM transactions WHERE user_id = :t GROUP BY name_of_stock", t=currentUser)
    #     # numberOfShares = db.execute("SELECT name_of_stock SUM(number_of_stock) FROM transactions WHERE user_id = :t GROUP BY name_of_stock", t=currentUser)
    #     shares = db.execute(
    #         "SELECT name_of_stock, SUM(number_of_stock) FROM transactions WHERE user_id = :t GROUP BY name_of_stock", t=currentUser)

    #     # loop through stocks
    #     counter = 0
    #     tracker = 0
    #     for x in stocks:
    #         x["sum"] = shares[counter]["SUM(number_of_stock)"]
    #         quote = lookup(x["symbol"])
    #         x["name"] = quote["name"]
    #         # which stocks the user owns, the numbers of shares owned, the current price of each stock, and the total value of each holding (
    #         x["price"] = quote["price"]
    #         x["total"] = x["sum"] * x["price"]
    #         # print(x["total"])
    #         tracker += x["sum"] * x["price"]
    #         counter = counter+1

    #     cashBalance = db.execute("SELECT cash FROM users WHERE id = :t", t=currentUser)
    #     precash = cashBalance[0]["cash"]

    #     # all of the stock totals together???//
    #     grandtotal = precash + tracker
    #     grandTotal = usd(grandtotal)
    #     cash = usd(precash)

    #     # return index page with correct info
    #     return render_template("index.html", stocks=stocks, cash=cash, grandTotal=grandTotal)

    # if request.method == "POST":
    #     cashme = request.form.get("cash")
    #     cashToAdd = float(cashme)

    #     currentMoneys = db.execute("SELECT cash FROM users WHERE id = :u", u=currentUser)
    #     currentMoney = currentMoneys[0]["cash"]

    #     newCash = float(currentMoney + cashToAdd)

    #     db.execute("UPDATE users SET cash = :y WHERE id = :x", x=currentUser, y=newCash)
    #     return redirect("/")


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    # allow them to add new events & set them up as event organizer
    # allow them to sign up for event already on calendar
    # email person who's in charge of that event
    return render_template("addevents.html")







    # """Buy shares of stock"""
    # if request.method == "GET":
    #     return render_template("buy.html")

    # if request.method == "POST":
    #     symb = request.form.get("symbol")
    #     symbol = symb.upper()
    #     if not symbol or lookup(symbol) == None:
    #         return apology("Sorry, please insert a stock to purchase")

    #     shares = request.form.get("shares")
    #     if not shares or shares.isdigit() == False:
    #         return apology("Sorry, please insert a valid number of stocks to purchase")

    #     share = int(shares)
         # currentUser = session["user_id"]
    #     quote = lookup(symbol)
    #     name = quote["name"]
    #     newSymbol = quote["symbol"]
    #     price = quote["price"]
    #     status = "BUY"

    #     if quote == None:
    #         return apology("Sorry, stock could not be looked up!")

    #     #  see if user had enough money
    #     premoney = db.execute("SELECT cash FROM users WHERE id = :u", u=currentUser)
    #     money = premoney[0]["cash"]

    #     if money < price:
    #         return apology("Sorry, you do not have enough cash to purchase that stock")

    #     else:
    #         # add info into the table
    #         moneyLeftover = money - (price * float(share))
    #         db.execute("""INSERT INTO transactions (user_id, name_of_stock, price_of_stock, type_of_transaction, number_of_stock, symbol)
    #         VALUES (:user_id, :name_of_stock, :price_of_stock, :type_of_transaction, :number_of_stock, :symbol)""",
    #                   user_id=currentUser, name_of_stock=name, price_of_stock=price, type_of_transaction=status, number_of_stock=share, symbol=symbol)
    #         # update cash
    #         db.execute("UPDATE users SET cash = :y WHERE id = :x", x=currentUser, y=moneyLeftover)

    #         flash('Bought!')

    #         return redirect("/")


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


# @app.route("/history")
# @login_required
# def history():
#     """Show history of transactions"""
#     currentUser = session["user_id"]

#     # select info for each stock and sum the # in each group
#     transactions = db.execute("SELECT * FROM transactions WHERE user_id = :t", t=currentUser)

#     # loop through transactions
#     counter = 0
#     for x in transactions:
#         x["type_of_transaction"] = transactions[counter]["type_of_transaction"]
#         x["name_of_stock"] = transactions[counter]["name_of_stock"]
#         x["symbol"] = transactions[counter]["symbol"]
#         x["price_of_stock"] = transactions[counter]["price_of_stock"]
#         x["number_of_stock"] = transactions[counter]["number_of_stock"]
#         x["date_of_transaction"] = transactions[counter]["date_of_transaction"]
#         x["time_of_transaction"] = transactions[counter]["time_of_transaction"]
#         counter = counter+1

#     # return history page with correct info
#     return render_template("history.html", transactions=transactions)


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


# @app.route("/quote", methods=["GET", "POST"])
# @login_required
# def quote():
#     # if for get vs. post method
#     if (request.method == "GET"):
#         return render_template("quote.html")

#     else:
#         # Get stock quote
#         symbol = request.form.get("symbol")
#         if not symbol:
#             return apology("Sorry, please insert a valid stock quote to view")

#         quote = lookup(symbol)

#         if quote != None:
#             # embed value from look up into quoted.html
#             name = quote["name"]
#             newSymbol = quote["symbol"]
#             price = usd(quote["price"])
#             return render_template("quoted.html", quote=quote)
#         else:
#             return apology("Sorry, stock could not be looked up!")


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
    currentUser = session["user_id"]
    if request.method == "GET":
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





    # currentUser = session["user_id"]
    # checked = db.execute("SELECT symbol FROM transactions WHERE user_id = :t", t=currentUser)
    # checker = set(val for dic in checked for val in dic.values())
    # for x in checker:
    #     x
    # # see all owned stocks? - look into my portfolio??

    # numOfStocksOwneds = db.execute("SELECT number_of_stock FROM transactions WHERE user_id = :t", t=currentUser)
    # numOfStocksOwned = numOfStocksOwneds[0]["number_of_stock"]
    # currentMoneys = db.execute("SELECT cash FROM users WHERE id = :u", u=currentUser)
    # currentMoney = currentMoneys[0]["cash"]

    # if request.method == "GET":
    #     return render_template("sell.html", checker=checker)

    # if request.method == "POST":
    #     symbol = request.form.get("symbol")
    #     # check if they own that stock
    #     if not symbol or checker == False:
    #         return apology("Sorry, please insert a stock which you own and want to sell")

    #     shares = request.form.get("shares")
    #     share = int(shares)

    #     # check if they own enough of that stock
    #     if not share or share > int(numOfStocksOwned):
    #         return apology("Sorry, please insert a valid number of stocks which you own and want to purchase")

    #     else:
    #         # remove stock - log sale as negative quantity
    #         quote = lookup(symbol)
    #         name = quote["name"]
    #         status = "SELL"
    #         priceForSale = quote["price"]
    #         numOfStocksMoved = (-share)

    #         # separate database with current # of stocks? bc this will give me a new transaction, but wont' update the storage itself
    #         db.execute("""INSERT INTO transactions (user_id, name_of_stock, symbol, price_of_stock, type_of_transaction, number_of_stock)
    #         VALUES (:user_id, :name_of_stock, :symbol, :price_of_stock, :type_of_transaction, :number_of_stock)""",
    #                   user_id=currentUser, name_of_stock=name, symbol=symbol, price_of_stock=priceForSale, type_of_transaction=status, number_of_stock=numOfStocksMoved)

    #         # update cash
    #         newMoney = int(currentMoney) + int(priceForSale * share)
    #         db.execute("UPDATE users SET cash = :y WHERE id = :x", x=currentUser, y=newMoney)

    #         flash('Sold!')

    #         return redirect("/")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
