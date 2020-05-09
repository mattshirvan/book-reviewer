from sys import argv, exit
import csv

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


def main():
    # Check for environment variable
    if not os.getenv("DATABASE_URL"):
        raise RuntimeError("DATABASE_URL is not set")
    
    # connect to database
    engine = create_engine(os.getenv("DATABASE_URL"))
    # engine = "postgres://chuqudbackzyxi:30be7d68b66efcc9d856988e4505d16908b8d7e3adfde2bc92a6fbca09548abe@ec2-50-17-90-177.compute-1.amazonaws.com:5432/db77ucqvdpm9ch"
    db = scoped_session(sessionmaker(bind=engine))

    # ensure correct usage
    if len(argv) != 2:
        print("Usage: python import.py your_file.csv")
        exit(0)

    # read csv into memory
    with open(argv[1], "r") as file:
        csv_file = csv.DictReader(file)

        # read rows in csv 
        for row in csv_file:
            isbn = row['isbn']
            title = row['title']
            author = row['author']
            year = row['year']

            # insert csv into database
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)", {'isbn': isbn, 'title': title, 'author': author, 'year': year})
            db.commit()
    
if __name__ == "__main__":    
    main()
