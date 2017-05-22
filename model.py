""" datamodel and functions for she owns """

from flask_sqlalchemy import SQLAlchemy
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

    business_categories = db.relationship("Category", secondary="business_categories",
                                          backref=db.backref("categories"))

    def __repr__(self):
        return "business_id={}, name={}".format(self.business_id, self.name)

    @classmethod
    def serialize_business_object(cls, businesses):

        schema = BusinessSchema(many=True)

        return schema.dump(businesses)


class Category(db.Model):
    """categories of the businesses in the db"""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(100))


class BusinessSchema(Schema):
    name = fields.Str()
    address = fields.Str()

    def __repr__(self):
        return "BusinessSchema instantiated"


# association table between Category and Business
business_categories = db.Table("business_categories",
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
