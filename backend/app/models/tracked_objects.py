from datetime import datetime

from .db import Base, db

OBJECT_TYPES = ("PAYLOAD", "ROCKET BODY", "DEBRIS", "UNKNOWN")


class TrackedObject(Base):
    __tablename__ = "tracked_objects"

    norad_id = db.Column(db.Integer, unique=True, nullable=False)
    object_name = db.Column(db.String(100))
    # DB column is named "ob_type" (backed by native Postgres enum "object_type")
    object_type = db.Column("ob_type", db.Enum(*OBJECT_TYPES, name="object_type", create_type=False), nullable=False)
    country_code = db.Column(db.String(10))
    launch_date = db.Column(db.Date)
    decay_date = db.Column(db.Date)
    status = db.Column(db.String(200))

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

    @classmethod
    def pulling_tracked_objects(cls):
        """Pull the current satellite catalog (satcat) from space-track.org, cache to CSV, then upsert tracked_objects."""
        snapshot_date = datetime.utcnow()
        csv_text = cls.pulling_from_spacetrack("satcat", current="Y", format="csv")
        csv_path = cls.save_raw_csv(csv_text, f"satcat_{snapshot_date:%Y-%m-%d}.csv")
        rows = cls.read_raw_csv(csv_path)

        records_loaded = 0
        for row in rows:
            if cls._upsert_row(row):
                records_loaded += 1
        db.session.commit()

        return {
            "snapshot_date": snapshot_date.date().isoformat(),
            "csv_path": str(csv_path),
            "records_fetched": len(rows),
            "records_loaded": records_loaded,
        }

    @classmethod
    def _upsert_row(cls, row):
        norad_id = row.get("NORAD_CAT_ID")
        object_name = row.get("OBJECT_NAME") or row.get("SATNAME")
        if not norad_id or not object_name:
            return False

        tracked_object = cls.query.filter_by(norad_id=int(norad_id)).first()
        if tracked_object is None:
            tracked_object = cls(norad_id=int(norad_id))
            db.session.add(tracked_object)

        decay = row.get("DECAY")
        tracked_object.object_name = object_name
        tracked_object.object_type = cls._normalize_object_type(row.get("OBJECT_TYPE"))
        tracked_object.country_code = (row.get("COUNTRY") or "")[:10] or None
        tracked_object.launch_date = cls._parse_date(row.get("LAUNCH"))
        tracked_object.decay_date = cls._parse_date(decay)
        tracked_object.status = "DECAYED" if decay else "ACTIVE"
        return True

    @staticmethod
    def _normalize_object_type(value):
        value = (value or "").strip().upper()
        return value if value in OBJECT_TYPES else "UNKNOWN"

    @staticmethod
    def _parse_date(value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            return None
