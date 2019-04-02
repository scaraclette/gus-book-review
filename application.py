'''VERSION 1.2                                           
    Wanted extra functionality
    1. username signup should be case insensitive
'''


import os

from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

# TODO: understand sessions and note taking
reviewed = []

# Global variable for session
user_id = 0

# TODO: can just direct to login page
# @app.route("/")
# def index():
#     return render_template("index.html")

@app.route("/", methods=["POST", "GET"])
def index():
    global user_id
    
    if request.method == 'POST':
        # TODO: implement full login/logout feature
        username = request.form.get("username")
        password = request.form.get("password")
        
        if db.execute("SELECT * FROM user_book WHERE user_name = :username AND user_password = :password", {"username": username.lower(), "password": password}).rowcount!=0:
            # Fetch the user_id
            current_user = db.execute("SELECT * FROM user_book WHERE user_name = :username AND user_password = :password", {"username": username.lower(), "password": password}).fetchone()
            # Sets the user session list
            user_id = current_user.id
            session[user_id] = []
            
            # Renders to search-book page
            return render_template("search-book.html", reviewed=session[user_id])

        #incorrect username/password TODO: implement create user
        return render_template("error.html") 
        
    # Default GET method renders index.html template, make sure session is cleared in case a user uses back command and clear the reviewed lsit.
    session.pop(user_id, None)
    user_id = 0
    return render_template("index.html")

# Signup method
@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if db.execute("SELECT * FROM user_book WHERE user_name = :username", {"username": username.lower()}).rowcount != 0:
            # Username already taken
            return render_template("username-taken.html")
            
        # Add User to Database and send to success page
        db.execute("INSERT INTO user_book (user_name, user_password) VALUES (:username, :password)", {"username":username.lower(), "password":password})
        db.commit()
        return render_template("success.html")

    # Default GET method goes to signup page
    return render_template("signup.html")


@app.route("/search-book")
def search_book():
    src = request.values.get("search")

    books = db.execute("SELECT * FROM books WHERE title ILIKE '%" + src +"%' OR isbn ILIKE '%" + src + "%' or author ILIKE '%" + src + "%'").fetchall()

    return render_template("result.html", books=books, src=src)