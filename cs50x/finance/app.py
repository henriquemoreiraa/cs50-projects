from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    user_portfolio = db.execute(
        "SELECT * FROM users, portfolio WHERE users.id = ? AND users.id = portfolio.user_id", session["user_id"])

    if len(user_portfolio) > 0:
        cash = user_portfolio[0]["cash"]
        total = 0

        for idx, stock in enumerate(user_portfolio):
            quote = lookup(stock["symbol"])
            user_portfolio[idx]["name"] = quote["name"]
            user_portfolio[idx]["price"] = usd(quote["price"])
            user_portfolio[idx]["total"] = usd(quote["price"] * stock["quantity"])
            user_portfolio[idx]["cash"] = usd(cash)
            total += quote["price"] * stock["quantity"]

        return render_template("index.html", user_portfolio=user_portfolio, total=usd(cash + total))
    return render_template("index.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("symbol doesn't exist", 400)

        quote = lookup(symbol)

        if not quote:
            return apology("invalid symbol", 400)

        try:
            float(request.form.get("shares"))
        except:
            return apology("only integers", 400)

        if float(request.form.get("shares")) % 2 != 0:
            return apology("only integers", 400)

        shares = quote["price"] * int(request.form.get("shares"))

        if shares < 1:
            return apology("positive integer only", 400)

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if user[0]["cash"] < shares:
            return apology("not enough cash", 400)

        db.execute("INSERT INTO transactions (user_id, symbol, quantity, price, type) VALUES(?, ?, ?, ?, ?)",
                user[0]['id'], symbol, int(request.form.get("shares")), shares, 'buy'
                )

        db.execute("INSERT INTO portfolio (user_id, symbol, quantity) VALUES(?, ?, ?)",
                user[0]['id'], symbol, int(request.form.get("shares"))
                )

        db.execute("UPDATE users SET cash = ? WHERE id = ?", (user[0]["cash"] - shares), user[0]['id'])

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT * FROM users, transactions WHERE users.id = ? AND users.id = transactions.user_id ORDER BY timestamp DESC", session["user_id"])

    if len(transactions) > 0:
        for idx, transaction in enumerate(transactions):
            transactions[idx]["price"] = usd(transaction["price"])

        return render_template("history.html", transactions=transactions)
    return render_template("history.html")


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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

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


@app.route("/change-password", methods=["GET", "POST"])
def change_password():
    """Change user password"""

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        old_password = request.form.get("old_password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not old_password:
            return apology("must provide old password", 403)

        # Ensure username was submitted
        elif not password:
            return apology("must provide password", 403)

        # Ensure password confirmation was submitted
        elif not confirmation:
            return apology("must provide confirmation", 403)

        elif password != confirmation:
            return apology("password confirmation is incorrect", 403)

        user = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])

        if not check_password_hash(user[0]["hash"], old_password):
            return apology("old password is incorrect", 403)

        hash = generate_password_hash(password)

        db.execute("UPDATE users SET hash = ?", hash)

        session.clear()

        # Redirect user to login form
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("changePassword.html")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if not (quote):
            return apology("symbol doesn't exist", 400)

        quote["price"] = usd(quote["price"])

        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password or not confirmation:
            return apology("must provide password and confirmation", 400)

        if password != confirmation:
            return apology("password confirmation is incorrect", 400)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        if len(rows) > 0 and rows[0]["username"]:
            return apology("username already exists", 400)

        hash = generate_password_hash(password)

        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return render_template("login.html")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    shares = db.execute("SELECT * FROM portfolio WHERE user_id = ?", session["user_id"])

    if request.method == "POST":
        symbols = {}
        symbol = request.form.get("symbol")
        shares_quantity = int(request.form.get("shares") or 0)

        for share in shares:
            if share["symbol"] not in symbols:
                symbols[share["symbol"]] = share["quantity"]

        if not symbol or symbol not in symbols:
            return apology("symbol not valid", 400)

        if shares_quantity < 1 or shares_quantity > symbols[symbol]:
            return apology("shares not valid", 400)

        share = db.execute("SELECT * FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)
        user = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        quote = lookup(symbol)

        if share[0]["quantity"] > 1:
            db.execute("UPDATE portfolio SET quantity = ? WHERE user_id = ? AND symbol = ?",
                       share[0]["quantity"] - shares_quantity, session["user_id"], symbol)
        else:
            db.execute("DELETE FROM portfolio WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)

        db.execute("UPDATE users SET cash = ? WHERE id = ?",
                   user[0]["cash"] + (quote["price"] * shares_quantity), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, quantity, price, type) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares_quantity, quote["price"] * shares_quantity, 'sell')

        return redirect("/")
    else:
        return render_template("sell.html", shares=shares)