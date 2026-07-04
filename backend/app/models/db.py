import csv
import os
from datetime import datetime
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from spacetrack import SpaceTrackClient

db = SQLAlchemy()

# backend/data/raw
RAW_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"


def init_db(app):
    db.init_app(app)


class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def pulling_from_spacetrack(table_name: str, **kwargs):
        username = os.getenv("SPACETRACK_USERNAME")
        password = os.getenv("SPACETRACK_PASSWORD")
        client = SpaceTrackClient(username, password)
        try:
            if not hasattr(client, table_name):
                raise ValueError(f"SpaceTrackClient has no method '{table_name}'")
            return getattr(client, table_name)(**kwargs)
        finally:
            client.session.close()

    @staticmethod
    def save_raw_csv(csv_text: str, filename: str) -> Path:
        # TODO: pull/push raw snapshots directly to an AWS S3 bucket instead of the local filesystem
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        csv_path = RAW_DATA_DIR / filename
        csv_path.write_text(csv_text or "", encoding="utf-8")
        return csv_path

    @staticmethod
    def read_raw_csv(csv_path: Path) -> list:
        if not csv_path.exists() or csv_path.stat().st_size == 0:
            return []
        with csv_path.open("r", newline="", encoding="utf-8") as f:
            return list(csv.DictReader(f))
