from flask import Blueprint, request, jsonify
from app.database_connection import db
from app.models.user import UserPermission
from datetime import datetime
from app.utils.response import success_response, error_response
from app.middleware.auth import token_required, is_admin

permission_bp = Blueprint('permission', __name__)

@permission_bp.route('/permissions', methods=['POST'])
@token_required
@is_admin()
def create_permission():
    try:
        data = request.get_json()
        
        if not data or 'permission_name' not in data:
            return error_response('Permission name is required', 'Permission name is required', 400)  
            
        # Check if permission already exists
        existing_permission = UserPermission.query.filter_by(permission_name=data['permission_name']).first()
        if existing_permission:
            return error_response('Permission already exists', 'Permission already exists', 409)
            
        # Create new permission
        new_permission = UserPermission(
            permission_name=data['permission_name']
        )
        
        db.session.add(new_permission)
        db.session.commit()
        
        return success_response(new_permission.serialize(), 'Permission created successfully', 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@permission_bp.route('/permissions', methods=['GET'])
@token_required
def get_permissions():
    try:
        permissions = UserPermission.query.all()
        return success_response([p.serialize() for p in permissions], 'Permissions fetched successfully', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)
