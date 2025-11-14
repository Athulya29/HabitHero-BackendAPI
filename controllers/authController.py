from flask import jsonify, request
from models.userModel import db, User
import re

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    return True, ""

def register_user():
    try:
        data = request.get_json()
        
        # Check if data exists and has all required fields
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['name', 'email', 'password', 'confirmPassword']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'success': False, 'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        confirm_password = data['confirmPassword']
        
        # Validate name
        if not name or len(name) < 2:
            return jsonify({'success': False, 'error': 'Name must be at least 2 characters long'}), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Check if passwords match
        if password != confirm_password:
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        # Validate password strength
        is_valid_password, password_error = validate_password(password)
        if not is_valid_password:
            return jsonify({'success': False, 'error': password_error}), 400
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'User with this email already exists'}), 409
        
        # Create new user
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = new_user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'error': 'Registration failed. Please try again.'}), 500

def login_user():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        required_fields = ['email', 'password']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return jsonify({'success': False, 'error': f'Missing fields: {", ".join(missing_fields)}'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate email format
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed. Please try again.'}), 500

def verify_token():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        token = data.get('token')
        
        if not token:
            return jsonify({'success': False, 'error': 'Token is required'}), 400
        
        user = User.verify_token(token)
        if user:
            return jsonify({
                'success': True,
                'valid': True,
                'user': user.to_dict()
            }), 200
        else:
            return jsonify({
                'success': False,
                'valid': False,
                'error': 'Invalid or expired token'
            }), 401
            
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return jsonify({'success': False, 'error': 'Token verification failed'}), 500

def get_user_profile(current_user):
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200