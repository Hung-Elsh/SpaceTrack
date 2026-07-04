from flask import Blueprint, request, jsonify
from ..models.tracked_objects import TrackedObject
from ..models.pipeline_run_logs import PipelineRunLog

objects_bp = Blueprint("objects", __name__)

SOURCE_NAME = "tracked_objects"


@objects_bp.route("/objects", methods=["GET"])
def get_objects():
    """GET /api/objects?date=YYYY-MM-DD&type=PAYLOAD&orbit=LEO"""
    date = request.args.get("date")
    object_type = request.args.get("type")
    orbit = request.args.get("orbit")
    data = TrackedObject.get_filtered(date=date, object_type=object_type, orbit=orbit)
    return jsonify(data), 200


@objects_bp.route("/objects/<int:norad_id>", methods=["GET"])
def get_object_detail(norad_id):
    """GET /api/objects/<norad_id>"""
    data = TrackedObject.get_detail(norad_id)
    if not data:
        return jsonify({"error": "Object not found"}), 404
    return jsonify(data), 200


@objects_bp.route("/objects", methods=["POST"])
def pulling_tracked_objects():
    """POST /api/objects"""
    available, next_available_at = PipelineRunLog.check_cooldown(SOURCE_NAME)
    if not available:
        return jsonify({
            "error": "cooldown",
            "message": "tracked_objects can only be pulled once per UTC day.",
            "next_available_at": next_available_at.isoformat(),
        }), 429

    try:
        data = TrackedObject.pulling_tracked_objects()
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
