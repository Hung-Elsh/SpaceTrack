from datetime import datetime, timedelta, timezone

from .db import Base, db

RUN_STATUSES = ("SUCCESSED", "FAILED", "PENDING", "STOPPED", "QUEUE")

# source_name values whose pull APIs are rate limited to once per UTC calendar day
COOLDOWN_SOURCES = ("tracked_objects", "orbital_snapshots")


class PipelineRunLog(Base):
    __tablename__ = "pipeline_run_logs"

    run_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.Enum(*RUN_STATUSES, name="pipeline_status", create_type=False), nullable=False)
    source_name = db.Column("souce_name", db.String(100), nullable=False)
    records_fetched = db.Column(db.Integer, nullable=False, default=0)
    records_loaded = db.Column(db.Integer, nullable=False, default=0)
    error_message = db.Column(db.String(100))

    @classmethod
    def record(cls, source_name: str, *, status: str, records_fetched: int = 0,
               records_loaded: int = 0, error_message: str = None):
        log = cls(
            run_date=datetime.now(timezone.utc).date(),
            status=status,
            source_name=source_name,
            records_fetched=records_fetched,
            records_loaded=records_loaded,
            error_message=(error_message[:100] if error_message else None),
        )
        db.session.add(log)
        db.session.commit()
        return log

    @classmethod
    def _last_success(cls, source_name: str):
        return (
            cls.query.filter_by(source_name=source_name, status="SUCCESSED")
            .order_by(cls.run_date.desc(), cls.id.desc())
            .first()
        )

    @classmethod
    def check_cooldown(cls, source_name: str):
        """A source may only run once per UTC calendar day.

        Returns (available, next_available_at). next_available_at is the next
        UTC midnight, or None when available now.
        """
        last_run = cls._last_success(source_name)
        if last_run is None:
            return True, None

        today = datetime.now(timezone.utc).date()
        if last_run.run_date < today:
            return True, None

        next_available_at = datetime.combine(today + timedelta(days=1), datetime.min.time(), tzinfo=timezone.utc)
        return False, next_available_at

    @classmethod
    def get_status(cls):
        status = {}
        for source_name in COOLDOWN_SOURCES:
            available, next_available_at = cls.check_cooldown(source_name)
            last_run = cls._last_success(source_name)
            status[source_name] = {
                "available": available,
                "next_available_at": next_available_at.isoformat() if next_available_at else None,
                "last_run_at": last_run.run_date.isoformat() if last_run else None,
            }
        return status
