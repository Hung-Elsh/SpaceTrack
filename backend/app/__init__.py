from flask import Flask
from flask_cors import CORS
from .config import Config
from .models.db import init_db
from .routes.objects import objects_bp
from .routes.snapshots import snapshots_bp
from .routes.backfill import backfill_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_db(app)

    # Allow Express frontend (port 3000) to call this API
    CORS(app, origins=["http://localhost:3000"])

    app.register_blueprint(objects_bp, url_prefix="/api")
    app.register_blueprint(snapshots_bp, url_prefix="/api")
    app.register_blueprint(backfill_bp, url_prefix="/api")

    return app
