#!/usr/bin/env python3
"""
Archivo principal para ejecutar la aplicación Flask
"""

from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
