'''VERSION 1.2                                           
    Wanted extra functionality
    1. Make sure that people can't access URL for searching book via id or allow them but notify that they are not logged in
'''


import os, sys

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

@app.route("/search-book/<int:book_id>", methods=["GET", "POST"])
def book(book_id):
    global user_id
    this_id = book_id

    if request.method == 'POST':
        rating = float(request.form.get("rating"))
        review = request.form.get("review")

        # If the user is not logged in, redirect to first page
        if user_id == 0:
            return render_template("login.html", book_id=book_id)

        if db.execute("SELECT * FROM user_reviews WHERE user_id = :user AND book_id = :book_id", {"user":user_id, "book_id":book_id}).rowcount != 0:
            return render_template("reviewed.html", book_id=book_id) #TODO: redirect to this page for get method

        db.execute("INSERT INTO user_reviews (user_id, book_id, rating, review) VALUES (:user_id, :book_id, :rating, :review)", {"user_id":user_id, "book_id":book_id, "rating":rating, "review":review})
        db.commit()
        return render_template("message.html", book_id=book_id,msg="review submitted!", btn="back")
        
        
    # Invalid book id
    book = db.execute("SELECT * FROM books WHERE id = :id", {"id":book_id}).fetchone()
    if book is None:
        return render_template("invalid-id.html")

    # Fetch all the reviews and display to details TODO
    reviews = db.execute("SELECT * FROM user_reviews JOIN user_book ON user_reviews.user_id=user_book.id AND user_reviews.book_id = :book_id", {"book_id":book_id}).fetchall()
    

    return render_template("details.html", reviews=reviews, book=book)

# id    user_id     book_id     rating      review

# # TODO implement review method
# @app.route("/review", methods=["POST"])
# def review():
#     return render_template("test.html")