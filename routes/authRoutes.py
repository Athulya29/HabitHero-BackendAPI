from flask import Blueprint
from controllers.authController import register_user, login_user, logout_user, get_current_user

auth_bp = Blueprint('auth', __name__)

# Auth routes
auth_bp.route('/register', methods=['POST'])(register_user)
auth_bp.route('/login', methods=['POST'])(login_user)
auth_bp.route('/logout', methods=['POST'])(logout_user)
auth_bp.route('/me', methods=['GET'])(get_current_user)