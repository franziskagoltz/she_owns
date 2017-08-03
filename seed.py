"""add business data to the database"""

import csv
import os
import requests
from model import connect_to_db, db, Business, Category


google_maps_key = os.environ.get("GMaps_Key")


def open_data(filepath):
    """takes filepath and returns file"""

    return open(filepath)


def get_lat_lng(address):
    """take address and get lant/lng from google maps geocode api """

    payload = {"address": address, "key": google_maps_key}

    geo_request = requests.get("https://maps.googleapis.com/maps/api/geocode/json?",
                              params=payload)

    geolocation = geo_request.json()

    return geolocation['results'][0]['geometry']['location']


def load_data(row):
    """populate db with data from csv file"""

    name, address, categories = row[1:4]

    lat_lng = get_lat_lng(address)

    business = Business(name=name, address=address, lat=lat_lng["lat"], lng=lat_lng["lng"])

    for category in categories.split(", "):

        # getting all existing category objects in the db
        categories_in_db = Category.get_all_categories()

        list_of_categories_in_db = [ c.category for c in categories_in_db ]

        # checking if category is already in db
        if category not in list_of_categories_in_db:
            category = Category(category=category)

        else:
            category = Category.get_category_by_name(category)

        # adding data to the association table
        if isinstance(category, list):
            for single_category in category:
                single_category.categories_business.append(business)
                db.session.add(single_category)
        else:
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
