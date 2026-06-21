from flask import Blueprint, request, jsonify
from ..models.tracked_objects import TrackedObject

objects_bp = Blueprint("objects", __name__)


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
