from flask import Flask, jsonify
import datetime, os

app = Flask(__name__)
APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")

@app.route("/")
def index():
    return jsonify({"app": "CloudDeploy", "version": APP_VERSION, "status": "running"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.datetime.utcnow().isoformat() + "Z"})

@app.route("/version")
def version():
    return jsonify({"version": APP_VERSION, "environment": os.environ.get("ENVIRONMENT", "production")})

@app.route("/pipelines")
def pipelines():
    return jsonify({"pipelines": [{"id": "pipe-001", "name": "backend-api", "status": "success"}, {"id": "pipe-002", "name": "frontend-app", "status": "running"}], "total": 2})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
