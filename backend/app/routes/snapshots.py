from flask import Blueprint, jsonify
from ..models.orbital_snapshots import OrbitalSnapshots
from ..models.pipeline_run_logs import PipelineRunLog

snapshots_bp = Blueprint("snapshots", __name__)

SOURCE_NAME = "orbital_snapshots"


@snapshots_bp.route("/snapshot/dates", methods=["GET"])
def get_snapshot_dates():
    """GET /api/snapshot/dates"""
    data = OrbitalSnapshots.get_available_dates()
    return jsonify(data), 200


@snapshots_bp.route("/snapshot", methods=["POST"])
def pulling_orbital_snapshots():
    """POST /api/snapshot"""
    available, next_available_at = PipelineRunLog.check_cooldown(SOURCE_NAME)
    if not available:
        return jsonify({
            "error": "cooldown",
            "message": "orbital_snapshots can only be pulled once per UTC day.",
            "next_available_at": next_available_at.isoformat(),
        }), 429

    try:
        data = OrbitalSnapshots.pulling_orbital_snapshots()
    except Exception as exc:
        PipelineRunLog.record(SOURCE_NAME, status="FAILED", error_message=str(exc))
        return jsonify({"error": str(exc)}), 500

    PipelineRunLog.record(
        SOURCE_NAME,
        status="SUCCESSED",
        records_fetched=data.get("records_fetched", 0),
        records_loaded=data.get("records_loaded", 0),
    )
    return jsonify(data), 200
