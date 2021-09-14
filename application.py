import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        
        holdings = db.execute(
            "SELECT symbol, SUM(CASE WHEN type = 'Buy' THEN shares ELSE -shares END) as shares, price FROM transactions WHERE user = ? GROUP BY symbol HAVING SUM(CASE WHEN type = 'Buy' THEN shares ELSE -shares END) <> 0 ORDER BY symbol", session["user_id"])
        
        for holding in holdings:
            holding["price"] = usd(lookup(holding["symbol"])["price"] * holding["shares"])
        
        rows = db.execute("SELECT username, cash FROM users WHERE id = ?", session["user_id"])
        name = rows[0]["username"]
        cash = usd(rows[0]["cash"])
        
        return render_template("index.html", holdings=holdings, name=name, cash=cash)
        
    else:
        # Ensure added funds was submitted
        if not request.form.get("add"):
            return apology("must provide adding sum", 403)
            
        # Ensure added funds was a positive number    
        while True:
            try:
                val = int(request.form.get("add"))
                if val < 0:
                    return apology("must provide positive amount", 403)
                    continue
                break
            except ValueError:
                return apology("must provide correct value", 403)
        
        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        added = int(request.form.get("add"))
        
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + added, session["user_id"])
        
        # Redirect user to home page
        return redirect("/")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
            
        # Ensure shares were submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)
        
        # Ensure shares were a positive number    
        while True:
            try:
                val = int(request.form.get("shares"))
                if val < 0:
                    return apology("must provide positive shares", 403)
                    continue
                break
            except ValueError:
                return apology("must provide number of shares", 403)
        
        stock = lookup(request.form.get("symbol"))
        
        # Ensure stock exists
        if stock == None:
            return apology("symbol must be correct", 403)
        
        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        sharesprice = stock["price"] * int(request.form.get("shares"))
        
        # Ensures user has enough money
        if cash < sharesprice:
            return apology("insufficient funds", 403)
        
        # Update databases
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash - sharesprice, session["user_id"])
        db.execute("INSERT INTO transactions (user, type, symbol, price, shares) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], "Buy", stock["symbol"], stock["price"], request.form.get("shares"))
        
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    transactions = db.execute(
        "SELECT type, symbol, price, shares, Timestamp FROM transactions WHERE user = ? ORDER BY Timestamp DESC", session["user_id"])
    for transaction in transactions:
        transaction["price"] = usd(transaction["price"])
    
    return render_template("history.html", transactions=transactions)


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


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
        
        stock = lookup(request.form.get("symbol"))
        
        if stock == None:
            return apology("symbol must be correct", 403)
            
        # Redirect user to quote page
        return render_template("quoted.html", name=stock["name"], price=usd(stock["price"]), symbol=stock["symbol"])
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("quote.html")
        
    
@app.route("/quoted")
@login_required
def quoted():
    """Get stock quote."""
    return apology("must enter the symbol")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
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
            
        # Ensure confirmation is submitted
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)
            
        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("confirmation doesn't match password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # Ensure username not exist
        if len(rows) != 0:
            return apology("already registered", 403)
        
        username = request.form.get("username")
        hashedpassword = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashedpassword)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide symbol", 403)
            
        # Ensure shares were submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares", 403)
        
        # Ensure shares were a positive number    
        while True:
            try:
                val = int(request.form.get("shares"))
                if val < 0:
                    return apology("must provide positive shares", 403)
                    continue
                break
            except ValueError:
                return apology("must provide number of shares", 403)
        
        stock = lookup(request.form.get("symbol"))
        
        # Ensure stock exists
        if stock == None:
            return apology("symbol must be correct", 403)
        
        holdings = db.execute(
            "SELECT SUM(CASE WHEN type = 'Buy' THEN shares ELSE -shares END) as shares FROM transactions WHERE user = ? AND symbol = ? GROUP BY symbol HAVING SUM(CASE WHEN type = 'Buy' THEN shares ELSE -shares END) <> 0", session["user_id"], stock["symbol"])
        
        # Ensure user has enough shares
        if holdings[0]["shares"] < int(request.form.get("shares")):
            return apology("insufficient amount of shares", 403)
        
        cash = db.execute("SELECT * FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        sharesprice = stock["price"] * int(request.form.get("shares"))
        
        # Update databases
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cash + sharesprice, session["user_id"])
        db.execute("INSERT INTO transactions (user, type, symbol, price, shares) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], "Sell", stock["symbol"], stock["price"], request.form.get("shares"))
        
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        holdings = db.execute(
            "SELECT symbol FROM transactions WHERE user = ? GROUP BY symbol HAVING SUM(CASE WHEN type = 'Buy' THEN shares ELSE -shares END) <> 0", session["user_id"])
        
        return render_template("sell.html", holdings=holdings)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
