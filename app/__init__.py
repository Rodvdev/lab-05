from flask import Flask, redirect, url_for
from config import Config
from app.models.database import db
from app.controllers.profesor_controller import profesor_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints
    app.register_blueprint(profesor_bp, url_prefix='/profesores')
    
    # Add root route
    @app.route('/')
    def index():
        return redirect(url_for('profesor.index'))
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app
