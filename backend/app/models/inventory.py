from app.database_connection import db
from app.utils.serializer import Serializer


class Stock(db.Model, Serializer):
    __tablename__ = 'stock'

    stock_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    available_stock = db.Column(db.Integer, nullable=False)
    units_sold = db.Column(db.Integer, nullable=False, default=0)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class ProductPricing(db.Model, Serializer):
    __tablename__ = 'product_pricing'

    pricing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=False)
    cost_price = db.Column(db.Float, nullable=False)
    selling_price = db.Column(db.Float, nullable=False)
    demand_forecast = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp()) 