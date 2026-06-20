from flask import Blueprint, jsonify
from ..services.snapshot_service import SnapshotService

snapshots_bp = Blueprint("snapshots", __name__)


# Endpoint: GET /api/snapshot/dates
@snapshots_bp.route("/snapshot/dates", methods=["GET"])
def get_snapshot_dates():
    # TODO: call SnapshotService.get_available_dates() and return results
    data = SnapshotService.get_available_dates()
    return jsonify(data), 200
