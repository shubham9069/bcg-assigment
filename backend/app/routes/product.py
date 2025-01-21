from flask import Blueprint, request
from app.database_connection import db
from app.models.product import Product, Category
from app.models.inventory import Stock, ProductPricing
from app.models.forecasting import OptimizedPrice,ForecastingLog
from app.utils.response import success_response, error_response
from app.middleware.auth import token_required, has_permission
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

product_bp = Blueprint('product', __name__)

def get_product_details(product_id, is_optimized=True,):
    query = db.session.query(Product, Category, Stock, ProductPricing,OptimizedPrice)

    query = query.join(Category, Product.category_id == Category.category_id)
    query = query.join(Stock, Product.product_id == Stock.product_id)
    query = query.join(ProductPricing, Product.product_id == ProductPricing.product_id)
    
    if is_optimized:
        query = query.join(OptimizedPrice, Product.product_id == OptimizedPrice.product_id)
    
    query = query.filter(Product.product_id == product_id)
    
    product_data = query.first()
    if not product_data:
        return None
    product = product_data[0].serialize()
    category = product_data[1].serialize()
    stock = product_data[2].serialize()
    pricing = product_data[3].serialize()
    

    response = {
        **product,
        'category': category,
        'stock': stock,
        'pricing': pricing
    }
    
    if is_optimized:
        optimized_price = product_data[4].serialize()
        response['optimized_price'] = optimized_price
    
    
    return response

@product_bp.route('/products', methods=['POST'])
@token_required
@has_permission('create')
def create_product():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'category_id','rating', 'description', 'cost_price', 'selling_price', 'available_stock','demand_forecast','optimized_price']
        for field in required_fields:
            if field not in data:
                return error_response(f'{field} is required', f'{field} is required', 400)
                
        # Verify category exists
        if not Category.query.get(data['category_id']):
            return error_response('Invalid category ID', 'Invalid category ID', 400)
            
        # Create product
        new_product = Product(
            name=data['name'],
            description=data['description'],
            category_id=data['category_id'],
            rating=data['rating'],
        )
        db.session.add(new_product)
        db.session.flush()  # Get product_id
        
        # Create stock entry
        stock = Stock(
            product_id=new_product.product_id,
            available_stock=data['available_stock'],
            units_sold=0
        )
        db.session.add(stock)
        
        # Create pricing entry
        pricing = ProductPricing(
            product_id=new_product.product_id,
            cost_price=data['cost_price'],
            selling_price=data['selling_price'],
            demand_forecast=data['demand_forecast'],
        )
        optimized_price = OptimizedPrice(
            product_id=new_product.product_id,
            optimized_price=data['optimized_price'],
        )
        forecasting_log = ForecastingLog(
            product_id=new_product.product_id,
            price=data['selling_price'],
            demand=data['demand_forecast'],
        )
        db.session.add(pricing)
        db.session.add(optimized_price)
        db.session.add(forecasting_log)
        
        db.session.commit()
        
        return success_response(
            get_product_details(new_product.product_id),
            'Product created successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@product_bp.route('/products', methods=['GET'])
@token_required
@has_permission('view')
def get_products():
    try:
        # Get search and filter parameters
        search_query = request.args.get('search', '').strip()
        category_id = request.args.get('category_id', 0)
        is_optimised_price = request.args.get('is_optimised_price', 'false').lower() == 'true'
        
        # Base query
        query = Product.query
        
        # Apply search filter
        if search_query:
            query = query.filter(
                or_(
                    Product.name.ilike(f'%{search_query}%'),
                    Product.description.ilike(f'%{search_query}%')
                )
            )
            
        # Apply category filter
        if int(category_id) > 0:
            query = query.filter(Product.category_id == int(category_id))
            
        # Execute query
        products = query.all()
        
        # Get complete details for each product
        product_list = [get_product_details(product.product_id,is_optimised_price) for product in products]
        
        return success_response(product_list, 'Products fetched successfully', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@token_required
@has_permission('view')
def get_product(product_id):
    try:
        product = get_product_details(product_id)
        if not product:
            return error_response('Product not found', 'Product not found', 404)
            
        return success_response(
            product,
            'Product fetched successfully',
            200
        )
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_required
@has_permission('edit')
def update_product(product_id):
    try:
        data = request.get_json()
        product = Product.query.get(product_id)
        
        if not product:
            return error_response('Product not found', 'Product not found', 404)
            
        # Update product details
        if 'name' in data:
            product.name = data['name']
        if 'description' in data:
            product.description = data['description']
        if 'category_id' in data:
            if not Category.query.get(data['category_id']):
                return error_response('Invalid category ID', 'Invalid category ID', 400)
            product.category_id = data['category_id']
            
        # Update stock if provided
        if 'available_stock' in data:
            stock = Stock.query.filter_by(product_id=product_id).first()
            stock.available_stock = data['available_stock']
            db.session.add(stock)
                
        # Update pricing if provided
        pricing = ProductPricing.query.filter_by(product_id=product_id).first()
        demand_forecast_changed = False
        if 'cost_price' in data and pricing:
            pricing.cost_price = data['cost_price']
        if 'selling_price' in data and pricing and pricing.selling_price != data['selling_price']:
            demand_forecast_changed = True
            pricing.selling_price = data['selling_price']
        if 'demand_forecast' in data and pricing and pricing.demand_forecast != data['demand_forecast']:
            demand_forecast_changed = True
            pricing.demand_forecast = data['demand_forecast']
        
        # if demand forecast changed or selling price changed, create a new forecasting log
        if demand_forecast_changed:
            forecasting_log = ForecastingLog(
                product_id=product_id,
                price=data['selling_price'],
                demand=data['demand_forecast'],
            )
            db.session.add(forecasting_log)
            
        db.session.commit()
        
        return success_response(
            get_product_details(product_id),
            'Product updated successfully',
            200
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@token_required
@has_permission('delete')
def delete_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return error_response('Product not found', 'Product not found', 404)
            
        # Delete related records
        Stock.query.filter_by(product_id=product_id).delete()
        ProductPricing.query.filter_by(product_id=product_id).delete()
        OptimizedPrice.query.filter_by(product_id=product_id).delete()
        ForecastingLog.query.filter_by(product_id=product_id).delete()
        
        # Delete product
        db.session.delete(product)
        db.session.commit()
        
        return success_response(None, 'Product deleted successfully', 200)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@product_bp.route('/categories', methods=['GET'])
@token_required
def get_categories():
    try:
        categories = Category.query.all()
        return success_response(
            [{'category_id': c.category_id, 'name': c.category_name} for c in categories],
            'Categories fetched successfully',
            200
        )
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)
    
@product_bp.route('/categories', methods=['POST'])
@token_required
def create_category():
    try:
        data = request.get_json()
        new_category = Category(category_name=data['category_name'])
        db.session.add(new_category)
        db.session.commit()
        return success_response(new_category.serialize(), 'Category created successfully', 201)
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)
