"""Flask application factory."""

from flask import Flask
from flask_cors import CORS

from app.config import config
from app.extensions import db, migrate


def create_app(config_name: str = "default") -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

    CORS(app, origins=app.config.get("CORS_ORIGINS", ["*"]))

    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        import app.models  # noqa: F401

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api/v1")

    @app.route("/health")
    def health():
        return {"status": "healthy"}, 200

    return app
