from flask import Blueprint
from controllers.authController import register_user, login_user, verify_token, get_user_profile
from middlewares.authMiddleware import token_required

# Create blueprint
auth_bp = Blueprint('auth', __name__)

# Public routes
auth_bp.route('/register', methods=['POST'])(register_user)
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/verify', methods=['POST'])(verify_token)

# Protected routes
auth_bp.route('/profile', methods=['GET'])(token_required(get_user_profile))