from flask import Blueprint, jsonify
from ..models.orbital_snapshots import OrbitalSnapshots

snapshots_bp = Blueprint("snapshots", __name__)


@snapshots_bp.route("/snapshot/dates", methods=["GET"])
def get_snapshot_dates():
    """GET /api/snapshot/dates"""
    data = OrbitalSnapshots.get_available_dates()
    return jsonify(data), 200
