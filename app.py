from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Add session configuration
    app.config['SECRET_KEY'] = 'habithero-secret-key-2024'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    # Initialize extensions - import here to avoid circular imports
    from models import db
    db.init_app(app)
    
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)
    
    # Register blueprints - import here to avoid circular imports
    from routes.authRoutes import auth_bp
    from routes.habitRoutes import habit_bp
    
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