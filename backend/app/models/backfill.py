from .db import Base, db

ACTION_MODES = ("AUTO", "ACTIVE")


class BackfillLogs(Base):
    __tablename__ = "backfill_logs"

    action_type = db.Column(db.Enum(*ACTION_MODES, name="action_mode", create_type=False), nullable=False)
    backfill_table = db.Column(db.String(20), nullable=False)
    successful = db.Column(db.Boolean, nullable=False, default=False)

    @classmethod
    def get_logs(cls):
        # TODO: SELECT backfill_table, created_at, successful, action_type FROM backfill_logs
        pass
