#!/usr/bin/env python3
"""
Script para inicializar la base de datos
"""

from app import create_app
from app.models.database import db

def init_database():
    """Inicializar la base de datos creando las tablas"""
    app = create_app()
    
    with app.app_context():
        print("Creando tablas de la base de datos...")
        db.create_all()
        print("✅ Base de datos inicializada correctamente")
        print("📊 Tablas creadas:")
        print("   - profesores")

if __name__ == '__main__':
    init_database()
