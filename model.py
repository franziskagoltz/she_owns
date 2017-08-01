""" datamodel and functions for she owns """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.exc import MultipleResultsFound
from marshmallow import Schema, fields, pprint

# connection to the PostgreSQL database
db = SQLAlchemy()


# ----------------- Model definitions ----------------- #

class Business(db.Model):
    """businesses to be shown on she owns"""

    __tablename__ = "businesses"

    business_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    address = db.Column(db.String(150))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __repr__(self):
        return "business_id={}, name={}".format(self.business_id, self.name)

    @classmethod
    def serialize_business_object(cls, businesses):

        schema = BusinessSchema(many=True)

        return schema.dump(businesses)

    @classmethod
    def get_business_by_id(self, business_id):
        """return business_id by name"""

        return Business.query.get(business_id)


class Category(db.Model):
    """categories of the businesses in the db"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(100))

    categories_business = db.relationship("Business", secondary="categories_business",
                                          backref=db.backref("businesses"))

    def __repr__(self):
        return "category_id={}, category={}".format(self.category_id, self.category)

    @classmethod
    def get_all_categories(cls):
        """Return all categories stored in db"""

        return Category.query.all()

    @classmethod
    def get_category_by_name(cls, category):
        """Return one category filtered by name"""

        try:
            return Category.query.filter(Category.category.ilike("%"+category+"%")).one()

        except MultipleResultsFound:
           return Category.query.filter(Category.category.ilike("%"+category+"%")).all()


class BusinessSchema(Schema):
    business_id = fields.Int()
    name = fields.Str()
    address = fields.Str()

    def __repr__(self):
        return "BusinessSchema instantiated"


# association table between Category and Business
categories_business = db.Table("categories_business",
                               db.Column("business_id", db.Integer,
                                         db.ForeignKey("businesses.business_id")),
                               db.Column("category_id", db.Integer,
                                         db.ForeignKey("categories.category_id")))


# ----------------- Helper Functions ----------------- #

def connect_to_db(app, db_uri='postgresql:///sheowns'):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # only runs when we run file directly, so we are assuming we want to
    # create tables

    from server import app
    connect_to_db(app)
    print "Connected to DB."
    db.create_all()
