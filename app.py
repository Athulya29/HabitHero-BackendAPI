from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models.userModel import db
from routes.authRoutes import auth_bp
from routes.habitRoutes import habit_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Add session configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Initialize extensions
    db.init_app(app)
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    
    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(habit_bp, url_prefix='/api/habits')
    
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