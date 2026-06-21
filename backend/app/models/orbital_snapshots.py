from flask_sqlalchemy import SQLAlchemy

from db import Base

db = SQLAlchemy()


class OrbitalSnapshots(Base):
    __tablename__ = "orbital_snapshots"

    tracked_object_id = db.Column(db.Integer, db.ForeignKey('tracked_objects.id'), nullable=False)
    snapshot_date = db.Column(db.DateTime, nullable=False)
    tle_line1 = db.Column(db.String(200), nullable=False)
    tle_line2 = db.Column(db.String(200), nullable=False)
    inclination = db.Column(db.Float, nullable=False, default=0.0)
    eccentricity = db.Column(db.Float, nullable=False, default=0.0)
    apogee_km = db.Column(db.Float, nullable=False, default=0.0)
    perigee_km = db.Column(db.Float, nullable=False, default=0.0)
    period_min = db.Column(db.Float, nullable=False, default=0.0)
    lat = db.Column(db.String(20), nullable=False)
    lon = db.Column(db.String(20), nullable=False)
    altitude_km = db.Column(db.Float, nullable=False, default=0.0)

    @classmethod
    def get_filtered(cls, date=None, object_type=None, orbit=None):
        # TODO: query tracked_objects JOIN orbital_snapshots with filters
        # Filters: date, object_type (PAYLOAD/DEBRIS/ROCKET_BODY/UNKNOWN), orbit (LEO/MEO/GEO)
        # Return: list of dicts [{norad_id, name, lat, lon, altitude_km, object_type, orbit}, ...]
        pass

    @classmethod
    def get_detail(cls, norad_id: int):
        # TODO: query tracked_objects + last N orbital_snapshots for this norad_id
        # Return: dict or None
        pass

    def pulling_orbital_snapshots(self):
        self.pulling_from_spacetrack("gp")
