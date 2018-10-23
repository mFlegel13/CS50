import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
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
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    #Get symbols and shares which the user owns
    portfolio_symbols = db.execute("SELECT shares,symbol \
                                        FROM portfolio WHERE id=:id", \
                                        id=session["user_id"])

    #Creat a temporary variable to store Total
    total_cash = 0

    #Update each symbol, prices and total
    for portfolio_symbol in portfolio_symbols:
        symbol = portfolio_symbol["symbol"]
        shares = portfolio_symbol["shares"]
        stock = lookup(symbol)
        total = shares * stock["price"]
        total_cash += total
        db.execute("UPDATE portfolio SET price=:price, \
                        total=:total WHERE id=:id AND symbol=:symbol", \
                        price=usd(stock["price"]), \
                        total=usd(total), id=session["user_id"], symbol=symbol)

    #Update cash in portfolio
    updated_cash = db.execute("SELECT cash FROM users \
                                    WHERE id=:id", id=session["user_id"])

    #Update the total cash
    total_cash += updated_cash[0]["cash"]

    #Print portfolio in index
    updated_portfolio = db.execute("SELECT * FROM portfolio \
                                        WHERE id=:id", id=session["user_id"])

    return render_template("index.html", stocks=updated_portfolio, \
                        cash=usd(updated_cash[0]["cash"]), total=usd(total_cash))

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
        return redirect(url_for("index"))

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        #Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        #Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        #Ensure password match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password don't match")

        #Insert new user in the database
        result = db.execute("INSERT INTO users (username, hash) \
                             VALUES(:username, :hash)", \
                             username=request.form.get("username"), \
                             hash=generate_password_hash(request.form.get("password")))

        if not result:
            return apology("Username already exist")

        #Remember the which user is logged in
        session["user_id"] = result

        #Redirect to homepage
        return redirect(url_for("index"))

    else:
        return render_template("register.html")

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        rows = lookup(request.form.get("symbol"))
        if not rows:
            return apology("Invalid symbol")
        return render_template("quoted.html", stock=rows)
    else:
        return render_template("quote.html")

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")
    #Ensure proper symbol
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")

        #Ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        #Get cash from user
        money = db.execute("SELECT cash FROM users \
                    WHERE id=:id", id=session["user_id"])

        #Ensure user has enough money
        if not money or float(money[0]["cash"]) < shares * stock["price"]:
            return apology("Not enough money")

        #Update History
        db.execute("INSERT INTO history (symbol,shares,price,id) \
                        VALUES (:symbol,:shares,:price,:id)", \
                        symbol=stock["symbol"], shares=shares, \
                        price=usd(stock["price"]), id=session["user_id"])

        #Update user's cash
        db.execute("UPDATE users SET cash=cash - :purchase \
                        WHERE id=:id", purchase=stock["price"] * float(shares), \
                        id=session["user_id"])

        #Get shares from that symbol
        user_shares = db.execute("SELECT shares FROM portfolio \
                                    WHERE id=:id AND symbol=:symbol", \
                                    id=session["user_id"], symbol=stock["symbol"])

        #If user has no shares of that symbol, create new one
        if not user_shares:
            db.execute("INSERT INTO portfolio (symbol,name,shares,price,total,id) \
                            VALUES (:symbol,:name,:shares,:price,:total,:id)", \
                            symbol=stock["symbol"],name=stock["name"],shares=shares, \
                            price=usd(stock["price"]),total=usd(shares*stock["price"]), \
                            id=session["user_id"])
        #Else increment
        else:
            shares_total = user_shares[0]["shares"] + shares
            db.execute("UPDATE portfolio SET shares=:shares \
                            WHERE id=:id AND symbol=:symbol", \
                            id=session["user_id"],symbol=stock["symbol"], \
                            shares=shares_total)

        return redirect(url_for("index"))

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":
        symbol = db.execute("SELECT symbol FROM portfolio WHERE id=:id", id=session["user_id"])
        return render_template("sell.html", stocks=symbol)
    #Ensure proper symbol
    else:
        stock = lookup(request.form.get("symbol"))
        if not stock:
            return apology("Invalid symbol")

        #Ensure proper number of shares
        try:
            shares = int(request.form.get("shares"))
            if shares < 0:
                return apology("Shares must be positive integer")
        except:
            return apology("Shares must be positive integer")

        #Get symbol shares from the user
        user_shares = db.execute("SELECT shares FROM portfolio \
                    WHERE id=:id AND symbol=:symbol", id=session["user_id"], \
                    symbol=stock["symbol"])

        #Ensure user has enough shares to sell
        if not user_shares or int(user_shares[0]["shares"]) < shares:
            return apology("Not enough shares")

        #Update history
        db.execute("INSERT INTO history (symbol,shares,price,id) \
                    VALUES (:symbol,:shares,:price,:id)", \
                    symbol=stock["symbol"],shares=-shares, \
                    price=usd(stock["price"]),id=session["user_id"])

        #Update user cash
        db.execute("UPDATE users SET cash=cash+:purchase WHERE id=:id", \
                    id=session["user_id"],purchase=stock["price"]*float(shares))

        #Decrement user shares
        shares_total = user_shares[0]["shares"] - shares

        #If shares of that symbol equals 0, delete
        if shares_total == 0:
            db.execute("DELETE FROM portfolio WHERE id=:id \
                        AND symbol=:symbol", id=session["user_id"], \
                        symbol=stock["symbol"])
        #Else Update portfolio
        else:
            db.execute("UPDATE portfolio SET shares=:shares WHERE id=:id \
                        AND symbol=:symbol", id=session["user_id"], \
                        symbol=stock["symbol"],shares=shares_total)

        return redirect(url_for("index"))

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    #Select data from history
    history = db.execute("SELECT * FROM history \
                            WHERE id=:id", id=session["user_id"])

    return render_template("history.html", history=history)


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
