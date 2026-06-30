from flask import Flask, jsonify
import datetime
import os

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
APP_NAME = "CloudPilot AI"


@app.route("/")
def index():
    return jsonify({
        "app": APP_NAME,
        "message": "Bienvenue sur CloudPilot AI — votre plateforme de déploiement cloud intelligent.",
        "version": APP_VERSION,
        "status": "running"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    })


@app.route("/version")
def version():
    return jsonify({
        "version": APP_VERSION,
        "deployed_at": datetime.datetime.utcnow().isoformat() + "Z",
        "environment": os.environ.get("ENVIRONMENT", "production")
    })


@app.route("/pipelines")
def pipelines():
    """Simule la liste des pipelines CI/CD gérés."""
    return jsonify({
        "pipelines": [
            {
                "id": "pipe-001",
                "name": "backend-api",
                "status": "success",
                "last_deploy": "2026-07-03T10:30:00Z",
                "environment": "production"
            },
            {
                "id": "pipe-002",
                "name": "frontend-app",
                "status": "running",
                "last_deploy": "2026-07-03T11:00:00Z",
                "environment": "staging"
            },
            {
                "id": "pipe-003",
                "name": "data-service",
                "status": "success",
                "last_deploy": "2026-07-02T18:45:00Z",
                "environment": "production"
            }
        ],
        "total": 3
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
