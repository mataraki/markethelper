import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

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


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///imust.db")

PREFERENCES = [
    "Main",
    "Do",
    "Buy",
    "Read",
    "Watch"
]

@app.route("/autocomplete", methods=["GET"])
def autocomplete():
    """Autocompletion on the Watch page"""
    query = db.execute("SELECT title FROM imdb WHERE title LIKE ?", "%" + request.args.get("q") + "%")
    if len(query) != 0:
        results = [movie["title"] for movie in query]
        return jsonify(matching_results=results)
    else:
        hollow = []
        return jsonify(matching_results=hollow)
    

@app.route("/")
def index():
    """Index Page"""
    # Get the current users preference
    if len(session) != 0:
        preference = db.execute("SELECT preference FROM users WHERE id = ?", session["user_id"])[0]["preference"]
            
        # Redirect user to preferrable page
        if preference == "main":
            return redirect("/main")
        elif preference == "do":
            return redirect("/do")
        elif preference == "buy":
            return redirect("/buy")
        elif preference == "read":
            return redirect("/read")
        elif preference == "watch":
            return redirect("/watch")
    else:
        return redirect("/main")
        

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Must Buy"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Delete entry
        if (request.form.get("delete")):
            db.execute("DELETE FROM buy WHERE id = ?", request.form.get("id"))
        # Add entry
        else:
            # Ensure that user told what to do
            if not request.form.get("what"):
                return render_template("buy.html", error="Must say what to buy")
            
            db.execute("INSERT INTO buy (user, whatbuy, details) VALUES(?, ?, ?)", session["user_id"], request.form.get("what"), request.form.get("details"))
        
        # Redirect user to Buy page
        return redirect("/buy")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        rows = db.execute("SELECT * FROM buy WHERE user = ? ORDER BY Timestamp DESC", session["user_id"])
        
        return render_template("buy.html", rows=rows) 


@app.route("/do", methods=["GET", "POST"])
@login_required
def do():
    """Must Do"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Delete entry
        if (request.form.get("delete")):
            db.execute("DELETE FROM do WHERE id = ?", request.form.get("id"))
        # Add entry
        else:
            # Ensure that user told what to do
            if not request.form.get("what"):
                return render_template("do.html", error="Must say what to do")
            
            db.execute("INSERT INTO do (user, whatdo, whendo, details) VALUES(?, ?, ?, ?)", session["user_id"], request.form.get("what"), request.form.get("when"), request.form.get("details"))
        
        # Redirect user to Do page
        return redirect("/do")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        rows = db.execute("SELECT * FROM do WHERE user = ? ORDER BY Timestamp DESC", session["user_id"])
        
        return render_template("do.html", rows=rows)
        
 
@app.route("/read", methods=["GET", "POST"])
@login_required
def read():
    """Must Read"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Delete entry
        if (request.form.get("delete")):
            db.execute("DELETE FROM read WHERE id = ?", request.form.get("id"))
        # Add entry
        else:
            # Ensure that user told what to do
            if not request.form.get("what"):
                return render_template("read.html", error="Must say what to read")
            
            db.execute("INSERT INTO read (user, whatread, details) VALUES(?, ?, ?)", session["user_id"], request.form.get("what"), request.form.get("details"))
        
        # Redirect user to Read page
        return redirect("/read")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        rows = db.execute("SELECT * FROM read WHERE user = ? ORDER BY Timestamp DESC", session["user_id"])
        
        return render_template("read.html", rows=rows) 
        

@app.route("/watch", methods=["GET", "POST"])
@login_required
def watch():
    """Must Watch"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Delete entry
        if (request.form.get("delete")):
            db.execute("DELETE FROM watch WHERE id = ?", request.form.get("id"))
        # Add entry
        else:
            # Ensure that user told what to do
            if not request.form.get("what"):
                return render_template("watch.html", error="Must say what to watch")
            
            movie = db.execute("SELECT * FROM imdb WHERE UPPER(title) = ?", request.form.get("what").upper())
            # Add rating if possible   
            if len(movie) != 0:
                rating = movie[0]["rating"]
            else:
                rating = "-"
            db.execute("INSERT INTO watch (user, whatwatch, rating, details) VALUES(?, ?, ?, ?)", session["user_id"], request.form.get("what"), rating, request.form.get("details"))
        
        # Redirect user to Watch page
        return redirect("/watch")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        rows = db.execute("SELECT * FROM watch WHERE user = ? ORDER BY Timestamp DESC", session["user_id"])
        
        return render_template("watch.html", rows=rows) 


@app.route("/main")
def main():
    """Main page"""
    if len(session) != 0:
        return render_template("main.html")
    else:
        return render_template("unlogined.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", error="Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", error="Must provide password")
            
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", error="Invalid username or/and password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("register.html", error="Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("register.html", error="Must provide password")
            
        # Ensure confirmation is submitted
        elif not request.form.get("confirmation"):
            return render_template("register.html", error="Must confirm password")
            
        # Ensure password matches confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return render_template("register.html", error="Confirmation doesn't match password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # Ensure username not exist
        if len(rows) != 0:
            return render_template("register.html", error="Already registered")
        
        username = request.form.get("username")
        hashedpassword = generate_password_hash(request.form.get("password"))
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashedpassword)

        # Redirect user to login page
        return redirect("/login")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Settings"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        
        if request.form.get("preference") not in PREFERENCES:
            return render_template("settings.html", error="Must provide correct preferences")
        
        db.execute("UPDATE users SET preference = ? WHERE id = ?", (request.form.get("preference")).lower(), session["user_id"])
        
        # Redirect user to home page
        return redirect("/")
        
    # User reached route via GET (as by clicking a link or via redirect)    
    else:
        preference = db.execute("SELECT preference FROM users WHERE id = ?", session["user_id"])[0]["preference"].capitalize()
        
        return render_template("settings.html", preferences=PREFERENCES, current=preference) 
        
        
def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
