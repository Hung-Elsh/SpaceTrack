from flask import Blueprint, jsonify
from ..models.pipeline_run_logs import PipelineRunLog

backfill_bp = Blueprint("backfill", __name__)


@backfill_bp.route("/backfill/status", methods=["GET"])
def get_backfill_status():
    """GET /api/backfill/status"""
    data = PipelineRunLog.get_status()
    return jsonify(data), 200
