"""server file for she owns"""

import os
from flask import Flask, render_template, redirect, request, jsonify
from sqlalchemy.orm.exc import NoResultFound
from flask_debugtoolbar import DebugToolbarExtension
from jinja2 import StrictUndefined

from model import Business, Category, connect_to_db

app = Flask(__name__)

# For usage of flask sessiosn and debug toolbar
app.secret_key = "IN_DEV"

# StrictUndefinded raises errors for undefined variables, otherwise jinja
# does not give us an error, but fails silently
app.jinja_env.undefined = StrictUndefined

# auto-reloads changes we made, so we don't have to reload manually everytime
# we make a little change
app.jinja_env.auto_reload = True

# Google Maps API Key
google_maps_key = os.environ.get("GMaps_Key")


@app.route("/")
def index():
    """render index page with """

    return render_template("index.html")


@app.route("/business-map")
def display_map():
    """displays map with businesses based on selected category"""

    return render_template("map_results.html")


# ------------------------------- JSON ROUTES ------------------------------- #


@app.route("/getBusinessInfo.json")
def get_business_info():
    """return a json element with businesses associated to the given category"""

    category = request.args.get("searchTerm", "")

    try:
        # get category object with search term
        category_object = Category.get_category_by_name(category)

    except NoResultFound:
        return "Can't find businesses"

    # getting businesses assocaited with elected category
    businesses = category_object.categories_business

    return jsonify(Business.serialize_business_object(businesses))


if __name__ == "__main__":
    # Setting debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    connect_to_db(app)

    app.run(host="0.0.0.0")