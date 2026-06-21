from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from db import Base

db = SQLAlchemy()

ACTION_MODES = ("AUTO", "ACTIVE")


class BackfillLogs(Base):
    __tablename__ = "backfill_logs"

    action_type = db.Column(db.Enum(ACTION_MODES), nullable=False, create_type=False)
    backfill_table = db.Column(db.String, nullable=False)
    successful = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_logs(cls):
        # TODO: SELECT backfill_table, created_at, successful, action_type FROM backfill_logs
        pass
