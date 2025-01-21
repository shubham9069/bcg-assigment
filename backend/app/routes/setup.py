from flask import Blueprint
from app.database_connection import db
from app.models.user import Role, UserPermission, RoleAndPermissionMapping
from app.models.product import Category, Product
from app.models.inventory import Stock, ProductPricing
from app.models.forecasting import OptimizedPrice, ForecastingLog
from app.utils.response import success_response, error_response
import random

setup_bp = Blueprint('setup', __name__)

@setup_bp.route('/initialize', methods=['POST'])
def initialize_db():
    try:
        if UserPermission.query.first() or Role.query.first():
            return error_response(
                'Database already initialized',
                'Database already contains roles and permissions',
                409
            )
            
        # Create predefined permissions
        permissions = {
            'create': 'Permission to create new items',
            'edit': 'Permission to edit existing items',
            'view': 'Permission to view items',
            'delete': 'Permission to delete items',
            'customA': 'Custom permission A'
        }
        
        permission_map = {}
        for perm_name in permissions:
            permission = UserPermission(permission_name=perm_name)
            db.session.add(permission)
            db.session.flush()
            permission_map[perm_name] = permission.permission_id
            
        # Create predefined roles with their permissions
        roles_config = {
            'admin': ['create', 'edit', 'view', 'delete', 'customA'],
            'buyer': ['view', 'customA'],
            'supplier': ['create', 'edit', 'view', 'customA'],
            'test-role': ['create', 'edit', 'view']
        }
        
        created_roles = {}
        for role_name, role_permissions in roles_config.items():
            # Create role
            role = Role(role_name=role_name)
            db.session.add(role)
            db.session.flush()
            created_roles[role_name] = role.role_id
            
            # Assign permissions to role
            for perm_name in role_permissions:
                mapping = RoleAndPermissionMapping(
                    role_id=role.role_id,
                    permission_id=permission_map[perm_name]
                )
                db.session.add(mapping)
                
        # Create test categories
        categories = [
            'Electronics',
            'Clothing',
            'Books',
            'Home & Kitchen',
            'Sports & Outdoors'
        ]
        
        category_map = {}
        for cat_name in categories:
            category = Category(
                category_name=cat_name,
                description=f'Test category for {cat_name}'
            )
            db.session.add(category)
            db.session.flush()
            category_map[cat_name] = category.category_id
            
        # Create test products (2 products per category)
        created_products = []
        for cat_name, cat_id in category_map.items():
            for i in range(2):
                # Create product
                product = Product(
                    name=f'Test {cat_name} Product {i+1}',
                    description=f'This is a test product {i+1} in the {cat_name} category',
                    category_id=cat_id,
                    rating=round(random.uniform(3.5, 5.0), 1)
                )
                db.session.add(product)
                db.session.flush()
                
                # Create stock
                stock = Stock(
                    product_id=product.product_id,
                    available_stock=random.randint(50, 200),
                    units_sold=random.randint(0, 50)
                )
                db.session.add(stock)
                
                # Create pricing
                cost_price = round(random.uniform(10.0, 100.0), 2)
                selling_price = round(cost_price * 1.4, 2)  # 40% markup
                demand_forecast = random.randint(100, 500)
                
                pricing = ProductPricing(
                    product_id=product.product_id,
                    cost_price=cost_price,
                    selling_price=selling_price,
                    demand_forecast=demand_forecast
                )
                db.session.add(pricing)
                
                # Create optimized price
                optimized_price = OptimizedPrice(
                    product_id=product.product_id,
                    optimized_price=selling_price * 0.9  # ±10% of selling price
                )
                db.session.add(optimized_price)
                
                # Create forecasting log
                forecasting_log = ForecastingLog(
                    product_id=product.product_id,
                    price=selling_price,
                    demand=demand_forecast
                )
                db.session.add(forecasting_log)
                
                created_products.append({
                    'id': product.product_id,
                    'name': product.name,
                    'category': cat_name,
                    'price': selling_price,
                    'stock': stock.available_stock
                })
                
        db.session.commit()
        
        # Prepare response
        response_data = {
            'permissions': [
                {'id': pid, 'name': pname} 
                for pname, pid in permission_map.items()
            ],
            'roles': [
                {
                    'id': rid,
                    'name': rname,
                    'permissions': roles_config[rname]
                }
                for rname, rid in created_roles.items()
            ],
            'categories': [
                {'id': cid, 'name': cname}
                for cname, cid in category_map.items()
            ],
            'products': created_products
        }
        
        return success_response(
            response_data,
            'Database initialized with predefined roles, permissions, categories, and products',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500) 