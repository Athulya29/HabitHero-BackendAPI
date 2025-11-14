from flask import jsonify, request
from models.userModel import db, User
import re

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def register_user():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['name', 'email', 'password', 'confirmPassword']):
            return jsonify({'success': False, 'error': 'All fields are required'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        confirm_password = data['confirmPassword']
        
        if password != confirm_password:
            return jsonify({'success': False, 'error': 'Passwords do not match'}), 400
        
        if not validate_email(email):
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'User with this email already exists'}), 409
        
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        token = new_user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'token': token,
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Registration failed. Please try again.'}), 500

def login_user():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        token = user.generate_token()
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'token': token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'success': False, 'error': 'Login failed. Please try again.'}), 500

def verify_token():
    try:
        data = request.get_json()
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
        return jsonify({'success': False, 'error': 'Token verification failed'}), 500

def get_user_profile(current_user):
    return jsonify({
        'success': True,
        'user': current_user.to_dict()
    }), 200