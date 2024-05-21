from cs50 import SQL
from flask import Flask, render_template, request, redirect, session, url_for
from random import randint
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required

app = Flask(__name__)

db = SQL("sqlite:///next.db")

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Get username and password from login form
        username = request.form.get("username")
        password = request.form.get("password")

        # Check that user input a username and password
        if not username or not password:
            error_message = "Please enter both username and password." 
            return render_template("login.html", error=error_message)
        
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check that username and password are correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            error_message = "Incorrect username or password."
            return render_template("login.html", error=error_message)
        
        # Remember which user logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to homepage
        return redirect("/")
    
    # User reached /login through GET
    else:
        return render_template("login.html")
    
@app.route("/logout")
def logout():

    # Forget any user_id
    session.clear()

    # Redirect to home page
    return redirect("/")

@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # User accesses route via POST
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirm")
        
        # Check that user filled all entries
        if not username or not password or not confirm:
            error_message = "Please fill all entries."
            return render_template("register.html", error=error_message)
        
        # Check that password and confrim password inputs match
        if password != confirm:
            error_message = "Passwords do not match."
            return render_template("register.html", error=error_message)
        
        # Query database for an entry with the registered username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Check that username does not already exist
        if len(rows) == 0:
            # Hash registered password
            hash = generate_password_hash(password)

            # Add new user to database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)

        # Username already exists
        else:
            error_message = "Username already exists."
            return render_template("register.html", error=error_message)
        
        # Redirect user to login
        return redirect("/login")
    # User accessed route via GET
    else:
        return render_template("register.html")

@app.route("/new", methods=["GET", "POST"])
def new():
    # User accesses route through POST
    if request.method == "POST":
        game_name = request.form.get("name")
        team_one = request.form.get("team-1")
        team_two = request.form.get("team-2")
        game_id = randint(100000, 999999)

        # Insert new game info to the games table
        db.execute("INSERT INTO games (id, name, user_id) VALUES(?, ?, ?)", game_id, game_name, session["user_id"])

        # Insert new players into the players table
        db.execute("INSERT INTO players (game_id, name) VALUES(?, ?), (?, ?)", game_id, team_one, game_id, team_two)

        # Redirect the user to the newly created game
        return redirect(url_for("game", id=game_id))
    else:
        # User accessed route through GET
        return render_template("new.html")
    
@app.route("/join", methods=["POST", "GET"])
@login_required
def join():
    # User accessed through POST
    if request.method == "POST":
        game_id = request.form.get("game_id")

        # Query db for games with the entered code
        rows = db.execute("SELECT * FROM games WHERE id = ?", game_id)

        # Check if such game exists and display error if not
        if len(rows) != 1:
            error_message = "Game does not exist."
            return render_template("join.html", error=error_message)
        
        # Redirect user to the game
        return redirect(url_for("game", id=game_id))
        
    else:
        # User accessed this route through GET
        return render_template("join.html")
    
@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    # User accessed route through POST
    if request.method == "POST":

        # Check if user submitted form2 (to add player in up next)
        if "form2" in request.form:    
            next_player = request.form.get("next")
            game_id = request.form.get("game_id")
            
            # Create a new player and add them to players table with the appropriate game code
            db.execute("INSERT INTO players (name, game_id) VALUES(?, ?)", next_player, game_id)

            # Redirect user to the same game page
            return redirect(url_for('game', id=game_id))
        
        # Check if user submitted form1 (Declare winner and loser and start next game)
        if "form1" in request.form:
            loser = request.form.get("winner")
            game_id = request.form.get("game_id")
            
            # Delete the losing player from the players table
            db.execute("DELETE FROM players WHERE player_id = ?", loser)

            # Redirect user to the same game page
            return redirect(url_for('game', id=game_id))
        
        # Check if user submitted form0 (Ends game entirely)
        if "form0" in request.form:
            game_id = request.form.get("game_id")

            # Delete the current game from the games table
            db.execute("DELETE FROM games WHERE id = ?", game_id)
            
            # Redirect users to the mygames page
            return redirect("/mygames")
    else:
        # User accessed page through GET
        game_id = request.args.get("id")
        game_data = db.execute("SELECT games.name AS game_name, games.id AS game_id, players.name AS player_name, player_id AS player_id FROM games INNER JOIN players ON games.id = players.game_id WHERE id = ? ORDER BY timestamp ASC", game_id)

        return render_template("game.html", game_data=game_data)
    
@app.route("/mygames", methods=["GET", "POST"])
@login_required
def mygames():
    # get a list of all games created by the logged in user
    games = db.execute("SELECT * FROM games WHERE user_id = ?", session["user_id"])

    return render_template("mygames.html", games=games)