from flask import Blueprint, request, jsonify
from ..models.backfill import BackfillLogs

objects_bp = Blueprint("objects", __name__)


@objects_bp.route("/objects/<int:norad_id>", methods=["GET"])
def get_backfill_logs(norad_id):
    """GET /api/objects/<norad_id>"""
    data = BackfillLogs.get_logs()
    if not data:
        return jsonify({"error": "Object not found"}), 404
    return jsonify(data), 200

