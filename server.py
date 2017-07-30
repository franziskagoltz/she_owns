"""server file for she owns"""

import os
from flask import Flask, render_template, redirect, request, jsonify
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
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

# add Google Maps API Key to global scope (all templates have access now)
app.add_template_global(google_maps_key, "google_maps_key")


@app.route("/")
def index():
    """render index page with """

    return render_template("index.html")


@app.route("/business-map")
def display_map():
    """displays map with businesses based on selected category"""

    return render_template("map_results.html")


@app.route("/businesses/<int:business_id>")
def show_business_details(business_id):
    """Shows detailed information about a selected business"""

    business = Business.get_business_by_id(business_id)

    return render_template("business_details.html", business=business)


# ------------------------------- JSON ROUTES ------------------------------- #


@app.route("/getBusinessInfo.json")
def get_business_info():
    """return a json element with businesses associated to the given category"""

    category = request.args.get("searchTerm", "")

    try:
        # get category object with search term
        category_object = Category.get_category_by_name(category)

    except NoResultFound:
        return jsonify({"data": "Can't find matches"})

    # getting businesses associated with elected category
    try:
        businesses = category_object.categories_business

    # when we have multiple matches, we get a list -> categories_business throws
    # AttributeError (list does not have that attribute
    except AttributeError:

        # todo: turn list of objects into one big object to pass to JS
        return jsonify({"data": "Can't find matches"})

    return jsonify(Business.serialize_business_object(businesses))


if __name__ == "__main__":
    # Setting debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    connect_to_db(app)

    app.run(host="0.0.0.0")