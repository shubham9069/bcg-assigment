from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from dotenv import load_dotenv
from sqlalchemy import text


load_dotenv()

db = SQLAlchemy()

def init_db(app: Flask):
    try:
        # Configure database URI
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL',"mysql+pymysql://root:9868999004@127.0.0.1:3306/bcg-data-base") 
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        # Initialize the database with the app
        db.init_app(app)
        
        # Ping the database connection
        ping_connection(app,db)
        
        
        # Create all tables
        with app.app_context():
            from app.models import Category, Product, Stock, ProductPricing, ForecastingLog, OptimizedPrice
            from app.models import User, Role, UserPermission, RoleAndPermissionMapping
            db.create_all()
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise e
    
def ping_connection(app,db):
    with app.app_context():
        try:
            # Execute a simple query to check the connection
            db.session.execute(text('(SELECT 1)'))
            print("Database connection successful.")
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise e
    