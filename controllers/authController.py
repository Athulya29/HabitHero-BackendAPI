from flask import jsonify, request, session
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
        
        # Import inside function to avoid circular imports
        from models import db, User
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': 'User with this email already exists'}), 409
        
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # Store user ID in session
        session['user_id'] = new_user.id
        session['authenticated'] = True
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': new_user.to_dict()
        }), 201
        
    except Exception as e:
        from models import db
        db.session.rollback()
        print(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'error': 'Registration failed. Please try again.'}), 500

def login_user():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ['email', 'password']):
            return jsonify({'success': False, 'error': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        # Import inside function to avoid circular imports
        from models import User
        
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return jsonify({'success': False, 'error': 'Invalid email or password'}), 401
        
        # Store user ID in session
        session['user_id'] = user.id
        session['authenticated'] = True
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed. Please try again.'}), 500

def logout_user():
    session.clear()
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200

def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'error': 'Not authenticated'}), 401
    
    # Import inside function to avoid circular imports
    from models import User
    
    user = User.query.get(user_id)
    if not user:
        session.clear()
        return jsonify({'success': False, 'error': 'User not found'}), 404
    
    return jsonify({
        'success': True,
        'user': user.to_dict()
    }), 200