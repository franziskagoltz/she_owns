"""add business data to the database"""

import csv
from model import connect_to_db, db, Business, Category


def open_data(filepath):
    """takes filepath and returns file"""

    return open(filepath)


def load_data(row):
    """populate db with data from csv file"""

    name, address, categories = row[1:4]

    business = Business(name=name, address=address)

    for c in categories.split(", "):

        # checking if category is already in db
        categories_in_db = Category.query.filter(Category.category == c).all()

        if not categories_in_db:
            category = Category(category=c)

            # adding data to the association table
            business.business_categories.append(category)

        db.session.add(business)

        db.session.commit()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print "Connected to DB."

    data = open_data("data/businesses.csv")

    for row in csv.reader(data):
        load_data(row)
