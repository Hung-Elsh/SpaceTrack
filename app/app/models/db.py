from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    db.init_app(app)

# TODO: define your ORM models here or in separate files (e.g. models/tracked_object.py)
# Example:
#   class TrackedObject(db.Model):
#       __tablename__ = "tracked_objects"
#       norad_id = db.Column(db.Integer, primary_key=True)
#       name = db.Column(db.String)
#       ...
