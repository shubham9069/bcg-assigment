from functools import wraps
from flask import request, g
from app.models.user import User, UserPermission, RoleAndPermissionMapping, Role
from app.utils.response import error_response
import jwt
import os
from app.database_connection import db

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return error_response('Token is missing', 'Authentication token is missing', 401)
            
        try:
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=["HS256"])
            current_user = User.query.with_entities(User.user_id, User.name, User.email, User.role_id).filter_by(user_id=data['user_id']).first()
            user_data ={
                'user_id': current_user[0],
                'name': current_user[1],
                'email': current_user[2],
                'role_id': current_user[3]
            }
                        
            if not current_user:
                return error_response('Invalid token', 'Invalid authentication token', 401)
            g.user = user_data
        except Exception as e:
            return error_response( str(e), 'Invalid authentication token', 401)
            
        return f(*args, **kwargs)
    return decorated

def has_permission(required_permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                return error_response('User not authenticated', 'Authentication required', 401)
                
            # Get user's permissions through role
            user_permissions = db.session.query(UserPermission.permission_name).\
                join(RoleAndPermissionMapping).\
                filter(RoleAndPermissionMapping.role_id == g.user['role_id']).all()
                
            user_permission_names = [p[0] for p in user_permissions]
            
            # Check if user has the required permission
            if required_permission not in user_permission_names:
                return error_response('Permission denied', f'Required permission: {required_permission}', 403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def is_admin():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.user:
                return error_response('User not authenticated', 'Authentication required', 401)
                
            # Get user's permissions
            user_permissions = db.session.query(Role).\
                join(RoleAndPermissionMapping, Role.role_id == RoleAndPermissionMapping.role_id).\
                filter(Role.role_id == g.user['role_id']).first()
                
                
                
            
            # Check if user has admin permission
            if 'admin' not in user_permissions.role_name:
                return error_response('Admin access required', 'This action requires admin privileges', 403)
                
            return f(*args, **kwargs)
        return decorated_function
    return decorator 