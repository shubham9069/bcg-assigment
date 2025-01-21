from flask import Blueprint, jsonify
from app.database_connection import ping_connection
from flask import current_app

health = Blueprint('health', __name__)

@health.route('/health')
def healthcheck():
    try:
        ping_connection(current_app, current_app.extensions['sqlalchemy'])
        return jsonify({"status": "healthy", "message": "Database connection is healthy"}) 
    except Exception as e:
        return jsonify({"status": "unhealthy", "error": str(e)}) 