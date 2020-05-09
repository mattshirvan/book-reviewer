# Project 1 Book Reviewer
A flask web application that utilizes a third party API provided by goodreads.com to get review statistics of books that are in the database, users may also access reviews statistics of books through the api by providing an isbn in the url.


## Prerequisites
Python 3.6 or greater
Flask
Flask-Session
psycopg2-binary
SQLAlchemy


### Installation
pip install -r requirements.txt

#### Usage
To use the app either register with your own credentials or login with a demo account Username: demo, Password: Demodemo123!, then search for a book by selecting the search method either by title, isbn or author and then start typing in the search bar and your searches should appear click on a book to see reviews and stats or to leave a review of your own. 

##### API usage
simply make a get request with the isbn passed into the url Example: /api/<isbn> then if the book exists and ther are stats for it you should receive a 200 response with json data otherwise you will receive a 404.

Web Programming with Python and JavaScript
