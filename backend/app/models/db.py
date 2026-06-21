import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from spacetrack import SpaceTrackClient

db = SQLAlchemy()


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
            client.close()
