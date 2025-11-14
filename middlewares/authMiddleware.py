from flask import jsonify, request
from functools import wraps
from models.userModel import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        
        # Alternative: Get token from query parameter
        if not token:
            token = request.args.get('token')
        
        if not token:
            return jsonify({
                'success': False, 
                'error': 'Authentication token is missing'
            }), 401
        
        try:
            current_user = User.verify_token(token)
            if not current_user:
                return jsonify({
                    'success': False,
                    'error': 'Invalid or expired token'
                }), 401
        except Exception as e:
            return jsonify({
                'success': False,
                'error': 'Token verification failed'
            }), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated