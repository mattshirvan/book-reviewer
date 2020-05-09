import os
import requests

from functools import wraps
from flask import request, redirect, url_for, session, render_template

# apology function for error handling per harvard cs50
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code

# require login
def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# API function 
def goodread_api(isbn):
    # Get API from goodreads.com for review stats
    api_key = os.environ.get("API_KEY")
    api = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})

    # check if response was 200 
    if api.status_code != 200:        
        raise Exception("ERROR: API request unsuccessful", str(api.status_code))

    # return data from goodread API
    api_data = api.json()
    print(api_data)
    return api_data
