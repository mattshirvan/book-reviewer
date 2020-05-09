from settings import app
from views import index, register, login, logout, search, books, reviews, get_book_api


# index
app.add_url_rule("/", view_func=index)

# register
app.add_url_rule("/register", view_func=register, methods=['GET', 'POST'])

# login 
app.add_url_rule("/login", view_func=login, methods=["GET", "POST"])

# logout
app.add_url_rule("/logout", view_func=logout)

# search
app.add_url_rule("/search", view_func=search, methods=['GET'])

# book page
app.add_url_rule("/books/<book_id>", view_func=books)

# reviews
app.add_url_rule("/reviews/<book_id>", view_func=reviews, methods=['GET','POST'])

# API
app.add_url_rule("/api/<isbn>", view_func=get_book_api)