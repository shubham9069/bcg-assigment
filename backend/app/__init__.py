from flask import Flask
from flask_cors import CORS
from app.healthcheck import health
from app.database_connection import init_db
from app.routes.permission import permission_bp
from app.routes.role import role_bp
from app.routes.user import user_bp
from app.routes.product import product_bp
from app.routes.setup import setup_bp


def create_app():
    app = Flask(__name__)
    
    # Enable CORS for all domains
    CORS(app)
    
    # Initialize database
    init_db(app)
    
    app.register_blueprint(health)
    app.register_blueprint(permission_bp, url_prefix='/api')
    app.register_blueprint(role_bp, url_prefix='/api')
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(setup_bp, url_prefix='/api')
    
    

    return app 