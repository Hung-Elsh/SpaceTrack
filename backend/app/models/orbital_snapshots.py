import math
from datetime import datetime

from sgp4.api import Satrec, jday

from .db import Base, db
from .tracked_objects import TrackedObject

# WGS84 ellipsoid constants, used to convert ECI/ECEF position to geodetic lat/lon/altitude
EARTH_RADIUS_EQ_KM = 6378.137
EARTH_FLATTENING = 1 / 298.257223563


class OrbitalSnapshots(Base):
    __tablename__ = "orbital_snapshots"

    tracked_object_id = db.Column(db.Integer, db.ForeignKey('tracked_objects.id'), nullable=False)
    snapshot_date = db.Column(db.Date, nullable=False)
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
    def get_available_dates(cls):
        """SELECT DISTINCT snapshot_date FROM orbital_snapshots ORDER BY DESC"""
        rows = db.session.query(cls.snapshot_date).distinct().order_by(cls.snapshot_date.desc()).all()
        return [row[0].isoformat() for row in rows]

    @classmethod
    def pulling_orbital_snapshots(cls):
        """Pull the current GP (TLE) catalog from space-track.org, cache to CSV, then load orbital_snapshots."""
        pulled_at = datetime.utcnow()
        csv_text = cls.pulling_from_spacetrack("gp", format="csv")
        csv_path = cls.save_raw_csv(csv_text, f"gp_{pulled_at:%Y-%m-%d}.csv")
        rows = cls.read_raw_csv(csv_path)

        records_loaded = 0
        records_skipped = 0
        for row in rows:
            if cls._load_row(row, pulled_at):
                records_loaded += 1
            else:
                records_skipped += 1
        db.session.commit()

        return {
            "snapshot_date": pulled_at.date().isoformat(),
            "csv_path": str(csv_path),
            "records_fetched": len(rows),
            "records_loaded": records_loaded,
            "records_skipped": records_skipped,
        }

    @classmethod
    def _load_row(cls, row, pulled_at):
        norad_id = row.get("NORAD_CAT_ID")
        tle_line1 = row.get("TLE_LINE1")
        tle_line2 = row.get("TLE_LINE2")
        if not norad_id or not tle_line1 or not tle_line2:
            return False

        # tracked_objects is populated separately via TrackedObject.pulling_tracked_objects()
        tracked_object = TrackedObject.query.filter_by(norad_id=int(norad_id)).first()
        if tracked_object is None:
            return False

        position = cls._compute_position(tle_line1, tle_line2, pulled_at)
        if position is None:
            return False
        lat, lon, altitude_km = position

        db.session.add(cls(
            tracked_object_id=tracked_object.id,
            snapshot_date=pulled_at.date(),
            tle_line1=tle_line1,
            tle_line2=tle_line2,
            inclination=float(row.get("INCLINATION") or 0.0),
            eccentricity=float(row.get("ECCENTRICITY") or 0.0),
            apogee_km=float(row.get("APOAPSIS") or 0.0),
            perigee_km=float(row.get("PERIAPSIS") or 0.0),
            period_min=float(row.get("PERIOD") or 0.0),
            lat=f"{lat:.6f}",
            lon=f"{lon:.6f}",
            altitude_km=altitude_km,
        ))
        return True

    @staticmethod
    def _compute_position(tle_line1, tle_line2, at):
        """Propagate the TLE to `at` (UTC) and convert TEME position to geodetic lat/lon/altitude_km (WGS84)."""
        satellite = Satrec.twoline2rv(tle_line1, tle_line2)
        jd, fr = jday(at.year, at.month, at.day, at.hour, at.minute, at.second + at.microsecond / 1e6)
        error, position, _velocity = satellite.sgp4(jd, fr)
        if error != 0:
            return None

        x, y, z = position
        gmst = OrbitalSnapshots._gmst_radians(jd + fr)

        lon = math.degrees(math.atan2(y, x) - gmst)
        lon = ((lon + 180) % 360) - 180

        r_xy = math.hypot(x, y)
        e2 = 2 * EARTH_FLATTENING - EARTH_FLATTENING ** 2
        lat = math.atan2(z, r_xy)
        for _ in range(5):
            sin_lat = math.sin(lat)
            c = EARTH_RADIUS_EQ_KM / math.sqrt(1 - e2 * sin_lat ** 2)
            lat = math.atan2(z + c * e2 * sin_lat, r_xy)

        sin_lat = math.sin(lat)
        c = EARTH_RADIUS_EQ_KM / math.sqrt(1 - e2 * sin_lat ** 2)
        altitude_km = r_xy / math.cos(lat) - c

        return math.degrees(lat), lon, altitude_km

    @staticmethod
    def _gmst_radians(jd_ut1):
        """Greenwich Mean Sidereal Time (IAU 1982 approximation), in radians."""
        t = (jd_ut1 - 2451545.0) / 36525.0
        gmst_sec = (
            67310.54841
            + (876600 * 3600 + 8640184.812866) * t
            + 0.093104 * t ** 2
            - 6.2e-6 * t ** 3
        )
        return math.radians((gmst_sec % 86400.0) / 240.0 % 360.0)

