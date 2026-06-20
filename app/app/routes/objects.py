from flask import Blueprint, request, jsonify
from ..services.object_service import ObjectService

objects_bp = Blueprint("objects", __name__)


# Endpoint: GET /api/objects?date=YYYY-MM-DD&type=PAYLOAD&orbit=LEO
@objects_bp.route("/objects", methods=["GET"])
def get_objects():
    date = request.args.get("date")
    object_type = request.args.get("type")
    orbit = request.args.get("orbit")

    # TODO: call ObjectService.get_objects() and return results
    data = ObjectService.get_objects(date=date, object_type=object_type, orbit=orbit)
    return jsonify(data), 200


# Endpoint: GET /api/objects/<norad_id>
@objects_bp.route("/objects/<int:norad_id>", methods=["GET"])
def get_object_detail(norad_id):
    # TODO: call ObjectService.get_object_detail() and return result
    data = ObjectService.get_object_detail(norad_id)
    if not data:
        return jsonify({"error": "Object not found"}), 404
    return jsonify(data), 200
