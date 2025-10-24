#!/usr/bin/env python3
"""
Production runner for Flask application
Uses Gunicorn WSGI server for better performance
"""

import os
from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Check if running in production
    if os.environ.get('FLASK_ENV') == 'production':
        # Use Gunicorn for production
        import multiprocessing
        workers = multiprocessing.cpu_count() * 2 + 1
        os.system(f"gunicorn --bind 0.0.0.0:5001 --workers {workers} --timeout 120 run:app")
    else:
        # Use Flask development server
        app.run(debug=True, host='0.0.0.0', port=5001)
