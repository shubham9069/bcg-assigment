from flask import Blueprint, request, g
from app.database_connection import db
from app.models.user import User, Role, UserPermission, RoleAndPermissionMapping
from app.utils.response import success_response, error_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from datetime import datetime, timedelta
from app.middleware.auth import token_required, has_permission, is_admin

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'password', 'role_id']
        for field in required_fields:
            if field not in data:
                return error_response(f'{field} is required', f'{field} is required', 400)
                
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return error_response('Email already registered', 'Email already registered', 409)
            
        # Verify role exists
        role = Role.query.get(data['role_id'])
        if not role:
            return error_response('Invalid role ID', 'Invalid role ID', 400)
            
        # Create new user
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role_id=data['role_id']
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Get user permissions through role
        permissions = db.session.query(UserPermission).\
            join(RoleAndPermissionMapping).\
            filter(RoleAndPermissionMapping.role_id == role.role_id).all()
            
        user_data = {
            **new_user.serialize(),
            'role_name': role.role_name,
            'permissions': [p.permission_id for p in permissions]
        }
        
        return success_response(user_data, 'User registered successfully', 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@user_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or 'email' not in data or 'password' not in data:
            return error_response('Email and password are required', 'Email and password are required', 400)
            
        user = User.query.filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password, data['password']):
            return error_response('Invalid credentials', 'Invalid email or password', 401)
            
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.user_id,
            'role_id': user.role_id,
            'exp': datetime.utcnow() + timedelta(days=1)
        }, os.getenv('JWT_SECRET_KEY'))
        
        # Get user permissions through role
        permissions = db.session.query(UserPermission).\
            join(RoleAndPermissionMapping).\
            filter(RoleAndPermissionMapping.role_id == user.role_id).all()
            
        role = Role.query.get(user.role_id)
            
        user_data = {
            **user.serialize(),
            'token': token,
            'role_name': role.role_name,
            'permissions': [p.serialize() for p in permissions]
        }
        
        return success_response(user_data, 'Login successful', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)

@user_bp.route('/users/me', methods=['GET'])
@token_required
def get_current_user():
    try:
        current_user = g.user
        # Get user permissions through role
        permissions = db.session.query(UserPermission).\
            join(RoleAndPermissionMapping).\
            filter(RoleAndPermissionMapping.role_id == current_user['role_id']).all()
            
        role = Role.query.get(current_user['role_id'])
            
        user_data = {
            **current_user,
            'role_name': role.role_name,
            'permissions': [p.serialize() for p in permissions]
        }
        
        return success_response(user_data, 'User details fetched successfully', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)

@user_bp.route('/users/<int:user_id>/role', methods=['PUT'])
@token_required
@is_admin()
def update_user_role(user_id):
    try:
        data = request.get_json()
        
        if 'role_id' not in data:
            return error_response('Role ID is required', 'Role ID is required', 400)
            
        user = User.query.get(user_id)
        if not user:
            return error_response('User not found', 'User not found', 404)
            
        # Verify role exists
        new_role = Role.query.get(data['role_id'])
        if not new_role:
            return error_response('Invalid role ID', 'Invalid role ID', 400)
        
        if user.role_id == data['role_id']:
            return error_response('User already has this role', 'User already has this role', 400)
            
        user.role_id = data['role_id']
        db.session.commit()
        
        # Get updated permissions through new role
        permissions = db.session.query(UserPermission).\
            join(RoleAndPermissionMapping).\
            filter(RoleAndPermissionMapping.role_id == data['role_id']).all()
            
        user_data = {
            'role': new_role.serialize(),
            'permissions': [p.serialize() for p in permissions]
        }
        
        return success_response(user_data, 'User role updated successfully', 200)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@user_bp.route('/users', methods=['GET'])
@token_required
def get_users():
    try:
        users = User.query.with_entities(User.user_id, User.name, User.email, User.role_id).all()
        user_list = []
        
        for user in users:
            user_id, name, email, role_id = tuple(user)
            role = Role.query.get(role_id)
            permissions = db.session.query(UserPermission).\
                join(RoleAndPermissionMapping).\
                filter(RoleAndPermissionMapping.role_id == role_id).all()
                
            user_data = {
                'user_id': user_id,
                'name': name,
                'email': email,
                'role_name': role.role_name,
                'permissions': [p.serialize() for p in permissions]
            }
            user_list.append(user_data)
            
        return success_response(user_list, 'Users fetched successfully', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500) 