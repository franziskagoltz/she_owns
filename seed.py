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

    for category in categories.split(", "):

        # getting all existing category objects in the db
        categories_in_db = Category.get_all_categories()

        list_of_categories_in_db = [ c.category for c in categories_in_db ]

        # checking if category is already in db
        if category not in list_of_categories_in_db:
            category = Category(category=category)

        else:
            category = Category.query.filter(Category.category == category).one()

        # adding data to the association table
        category.categories_business.append(business)

        db.session.add(category)
        db.session.commit()


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
    print "Connected to DB."

    data = open_data("data/businesses.csv")

    for row in csv.reader(data):
        load_data(row)
