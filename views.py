import re


from flask import Flask, session, request, redirect, url_for, render_template, flash, jsonify
from settings import db, EMAIL_REGEX, PASSWORD, text
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import login_required, apology, goodread_api


# home page 
@login_required
def index():
    """Homepage after login where users can search for books"""

    return render_template("index.html")


def register():
    """Registration page"""

    # Get register page
    if request.method == 'GET':
        return render_template("register.html")
   
   # Post to register page
    if request.method == 'POST':        
        
        # set a boolean for validation
        valid = True

        # check if username or password was provided
        if not request.form.get("username") or not request.form.get("password"):
            flash("must provide a username or password")
            valid = False
            return redirect(url_for("register"))

        # check if email is valid email
        if not EMAIL_REGEX.match(request.form.get("email")):
            flash("must provide an email")
            valid = False
            return redirect(url_for("register"))
        
        # check if user is already registered
        email_query = "SELECT * FROM users WHERE email = :email"
        data = {'email': request.form.get("email")}
        result = db.execute(email_query, data).first()
     
        # if user exists alreay redirect
        if result:
            flash("user already exists")
            valid = False
            return redirect(url_for("register"))

        # check for dangerous input from user
        if re.search(r";|'|-", request.form.get("username")) or re.search(r";|'|-", request.form.get("password")) or re.search(r";|'|-", request.form.get("email")):
            flash("ILLEGAL!!!")
            valid = False
            return redirect(url_for("register"))

        # final check of validations
        if not valid:
            return redirect(url_for("register"))

        # register user oncee valid
        elif valid:
            password = generate_password_hash(request.form.get("password"))
            query = "INSERT INTO users (username, email, password) VALUES (:username, :email, :password)"
            data = {
                'username': request.form.get("username"),
                'email': request.form.get("email"),
                'password': password
            }

            # Catch and handle errors
            try:
                db.execute(query, data)
                flash("Registration was successful")

            except InternalServerError:
                return 

            finally:
                db.commit()
            
            return redirect(url_for("login"))


# login 
def login():
    """Login Users """
    
    # user Post login
    if request.method == "POST":

        # clear session
        session.clear()

        # ensure username was submitted
        if not request.form.get("username"):
            flash("Please enter a valid username")
            return redirect(url_for("login"))

        # ensure password was submitted
        if not request.form.get("password"):
            flash("Please enter a valid password")
            return redirect(url_for("login"))

        # query database for user
        query = "SELECT * FROM users WHERE username = :username"
        data = { 'username': request.form.get("username")}
        result = db.execute(query, data).first()

        # validate users credentials
        if result:
            if check_password_hash(result.password, request.form.get("password")):
                session['user_id'] = result.id
                session['username'] = result.username
                flash("You are now logged in")                
                return redirect(url_for("index"))

        # Not the user return
        elif not result:
            return redirect(url_for("login"))

    # Get login page
    else:
        return render_template("login.html")


# logout
def logout():
    """log user out"""

    # clear session
    session.clear()
    return redirect(url_for("login"))


# search
@login_required
def search():
    """Search for books"""

    # set values to none
    query = ''
    data = ''

    # if the search is by isbn
    if request.args.get("search") == "isbn":
        query = text("SELECT * FROM books WHERE isbn LIKE :isbn")
        data = {'isbn': f"%{request.args.get('book')}%"}

    # if the search is by title
    elif request.args.get("search") == "title":
        query = text("SELECT * FROM books WHERE title LIKE :title")
        data = {'title': f"%{request.args.get('book').title()}%"}

    # if the search is by author
    elif request.args.get("search") == "author":
        query = text("SELECT * FROM books WHERE author LIKE :author")
        data = {'author': f"%{request.args.get('book').title()}%"}

    # get all the books that match users search
    books = None
    if request.args.get('book') is not None and len(request.args.get('book')) > 0: 

        # catch and hanlde errors
        try:   
            books = db.execute(query, data).fetchall()        

        finally:
            db.close()
            print(request.args.get('book'))

    return render_template("partials/search.html", books = books)


# book page
@login_required
def books(book_id):
    """Show book page"""

    # query database for book
    query = "SELECT * FROM books WHERE id = :book_id"    
    data = {'book_id': book_id}
    book = db.execute(query, data).first()        
    isbn = [book.isbn.rstrip()]
    print(isbn)
    
    # set API to request book review counts
    api_data = goodread_api(isbn)

    return render_template("book.html", book=book, api_data = api_data)


# reviews
@login_required
def reviews(book_id):
    """Reviews route with AJAX"""

    # initialize reviews variable
    reviews = None

    # user Post review to server
    if request.method == "POST":
        
        # check if user has already posted a review
        double_post_query = "SELECT * FROM reviews WHERE user_id = :user_id AND book_id = :book_id"
        double_post_data = {'user_id': session['user_id'], 'book_id': book_id}        
        result = db.execute(double_post_query, double_post_data).first()
        print(result)
        if result is not None:
            flash("You've already reviewed this book.")
            return redirect("/books/{}".format(book_id))

        # create review and into database
        query = "INSERT INTO reviews (rating, review, user_id, book_id) VALUES (:rating, :review, :user_id, :book_id)"
        data = {
            'rating': request.form.get("rating"),
            'review': request.form.get("review"),
            'user_id': session['user_id'],
            'book_id': book_id
        }

        # prevent errors during async connection
        try:        
            db.execute(query, data)
            db.commit()
            flash("Review Submitted")
            
        except Exception as e:            
            flash("Review Submission Failed:") 

        finally:
            db.close()
        
        return redirect("/books/{}".format(book_id))

    # update reviews on page
    if request.method == "GET":
        
        # retrieve reviews if any from database
        if book_id is not None and book_id != "undefined":       
            query = "SELECT * FROM reviews WHERE book_id = :book_id ORDER BY updated_at DESC" 
            data = {'book_id': book_id}
            
            # prevent errors during async connection
            try:
                reviews = db.execute(query, data).fetchall()
                
            finally:
                db.close()  

        return render_template("partials/review.html", reviews=reviews)


# API GET route
def get_book_api(isbn):
    """Return details about requested book"""

    # check if book is in database
    query = "SELECT * FROM books WHERE isbn = :isbn"
    data = {'isbn': isbn}
    book = db.execute(query, data).first()
    print(book)  

    # return 404 error if book not found
    if book is None:
        return jsonify({'error': "Something went wrong, check that the isbn is correct"}), 404
    
    # if the book was found 
    if book:

        # set API to request book review counts
        api_data = goodread_api(isbn)
        
        # return api JSON response
        return jsonify({
            'title': book.title.rstrip(),
            'author':book.author.rstrip(),
            'year': str(book.year).rstrip(),
            'isbn': isbn,
            'review_count': api_data['books'][0]['reviews_count'],
            'average_score': api_data['books'][0]['average_rating']
        })
