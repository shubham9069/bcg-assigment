from flask import Blueprint, request
from app.database_connection import db
from app.models.user import Role, UserPermission, RoleAndPermissionMapping
from app.utils.response import success_response, error_response
from app.middleware.auth import token_required, is_admin
from flask import g
role_bp = Blueprint('role', __name__)

@role_bp.route('/roles', methods=['POST'])
@token_required
@is_admin()
def create_role():
    try:
        data = request.get_json()
        
        if not data or 'role_name' not in data:
            return error_response('Role name is required', 'Role name is required', 400)
            
        if 'permissions' not in data or not isinstance(data['permissions'], list):
            return error_response('Permissions array is required', 'Permissions array is required', 400)
            
        # Check if role already exists
        existing_role = Role.query.filter_by(role_name=data['role_name']).first()
        if existing_role:
            return error_response('Role already exists', 'Role already exists', 409)
            
        # Verify all permissions exist 
        permission_ids = data['permissions']
        existing_permissions = UserPermission.query.filter(UserPermission.permission_id.in_(permission_ids)).all()
        if len(existing_permissions) != len(permission_ids):
            return error_response('Some permission IDs are invalid', 'Invalid permission IDs', 400)
            
        # Create new role
        new_role = Role(role_name=data['role_name'])
        db.session.add(new_role)
        db.session.flush()  # Flush to get the role_id
        
        # Create role-permission mappings
        for permission_id in permission_ids:
            mapping = RoleAndPermissionMapping(
                role_id=new_role.role_id,
                permission_id=permission_id
            )
            db.session.add(mapping)
            
        db.session.commit()
        
        # Prepare response with role and its permissions
        role_data = {
            **new_role.serialize(),
            'permissions': permission_ids
        }
        
        return success_response(role_data, 'Role created successfully with permissions', 201)
        
    except Exception as e:
        db.session.rollback()
        return error_response(str(e), 'Internal server error', 500)

@role_bp.route('/roles', methods=['GET'])
def get_roles():
    try:
        role_list = db.session.query(Role, UserPermission).\
            join(RoleAndPermissionMapping, Role.role_id == RoleAndPermissionMapping.role_id).\
            join(UserPermission, RoleAndPermissionMapping.permission_id == UserPermission.permission_id).\
            all()
        response={}
        for role in role_list:
            if role[0].role_id not in response:
                response[role[0].role_id] = {
                    **role[0].serialize(),
                    'permissions_data': [role[1].serialize()]
                }
            else:
                response[role[0].role_id]['permissions_data'].append(role[1].serialize())
            
           
            
        return success_response(list(response.values()), 'Roles fetched successfully', 200)
        
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)
    
@role_bp.route('/roles/me', methods=['GET'])
@token_required
def get_my_role():
    try:
        user_role = db.session.query(Role.role_id,Role.role_name, UserPermission.permission_name).\
            join(RoleAndPermissionMapping, Role.role_id == RoleAndPermissionMapping.role_id).\
            join(UserPermission, RoleAndPermissionMapping.permission_id == UserPermission.permission_id).\
            filter(Role.role_id == g.user['role_id']).all()
        response = {
            'role_name': user_role[0][1],
            'role_id': user_role[0][0],
            'permissions': [p[2] for p in user_role]
        }
        return success_response(response, 'Role fetched successfully', 200)
    except Exception as e:
        return error_response(str(e), 'Internal server error', 500)

