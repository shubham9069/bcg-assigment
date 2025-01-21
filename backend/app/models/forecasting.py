from app.database_connection import db
from app.utils.serializer import Serializer

class ForecastingLog(db.Model, Serializer):
    __tablename__ = 'forecasting_logs'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    demand = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class OptimizedPrice(db.Model, Serializer):
    __tablename__ = 'optimized_price'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    optimized_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp()) 
    

    