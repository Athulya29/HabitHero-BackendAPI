from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models.userModel import db
from routes.authRoutes import auth_bp
from middlewares.authMiddleware import token_required

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:5173"])
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    # Test protected route
    @app.route('/api/protected')
    @token_required
    def protected_route(current_user):
        return jsonify({
            'success': True,
            'message': 'This is a protected route',
            'user': {
                'id': current_user.id,
                'name': current_user.name,
                'email': current_user.email
            }
        })
    
    # Health check route
    @app.route('/api/health')
    def health_check():
        return jsonify({'success': True, 'message': 'Server is running'})
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)