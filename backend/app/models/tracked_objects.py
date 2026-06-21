from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from db import Base

db = SQLAlchemy()

OBJECT_TYPES = ("PAYLOAD", "ROCKET BODY", "DEBRIS", "UNKNOWN")


class TrackedObject(Base):
    __tablename__ = "tracked_objects"

    norad_id = db.Column(db.Integer, unique=True, nullable=False)
    object_name = db.Column(db.String(100), nullable=False)
    object_type = db.Column(db.Enum(OBJECT_TYPES), nullable=False, create_type=False)
    country_code = db.Column(db.String(10))
    launch_date = db.Column(db.Datetime)
    decay_date = db.Column(db.Datetime)
    status = db.Column(db.String)

    @classmethod
    def get_available_dates(cls):
        # TODO: SELECT DISTINCT snapshot_date FROM orbital_snapshots ORDER BY DESC
        # Return: list of date strings ["2025-06-20", "2025-06-19", ...]
        pass

    def pulling_tracked_objects(self):
        self.pulling_from_spacetrack("satcat")
