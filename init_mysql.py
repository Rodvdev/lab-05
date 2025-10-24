#!/usr/bin/env python3
"""
Script para inicializar la base de datos MySQL
"""

import pymysql
from config import Config
import os

def create_database():
    """Crear la base de datos MySQL"""
    try:
        # Conectar a MySQL sin especificar base de datos
        connection = pymysql.connect(
            host='localhost',
            user=os.environ.get('DB_USER', 'root'),
            password=os.environ.get('DB_PASSWORD', 'password'),
            port=int(os.environ.get('DB_PORT', 3306))
        )
        
        cursor = connection.cursor()
        
        # Crear base de datos
        cursor.execute("CREATE DATABASE IF NOT EXISTS lab_05")
        print("✅ Base de datos 'lab_05' creada correctamente")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"❌ Error al crear la base de datos: {e}")
        return False
    
    return True

def init_database():
    """Inicializar la base de datos creando las tablas"""
    try:
        from app import create_app
        from app.models.database import db
        
        app = create_app()
        
        with app.app_context():
            print("Creando tablas de la base de datos...")
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
            print("📊 Tablas creadas:")
            print("   - profesor (solo para la aplicación Flask)")
            print("   - Nota: La base de datos contiene todas las tablas del sistema universitario")
            
            # Insertar datos de ejemplo
            from app.models.profesor import Profesor
            
            # Verificar si ya existen datos
            if Profesor.query.count() == 0:
                sample_data = [
                    {
                        'nombre': 'Alberto',
                        'apellido': 'Gutiérrez Ramos',
                        'dni': '11111111',
                        'email': 'alberto.gutierrez@universidad.edu',
                        'telefono': '999111222',
                        'especialidad': 'Ingeniería de Software',
                        'titulo_academico': 'Doctor en Ciencias de la Computación'
                    },
                    {
                        'nombre': 'Carmen',
                        'apellido': 'Ruiz Paredes',
                        'dni': '22222222',
                        'email': 'carmen.ruiz@universidad.edu',
                        'telefono': '999222333',
                        'especialidad': 'Base de Datos',
                        'titulo_academico': 'Magister en Informática'
                    },
                    {
                        'nombre': 'Fernando',
                        'apellido': 'Morales Campos',
                        'dni': '33333333',
                        'email': 'fernando.morales@universidad.edu',
                        'telefono': '999333444',
                        'especialidad': 'Redes y Comunicaciones',
                        'titulo_academico': 'Doctor en Telecomunicaciones'
                    }
                ]
                
                for data in sample_data:
                    profesor = Profesor(**data)
                    db.session.add(profesor)
                
                db.session.commit()
                print("✅ Datos de ejemplo insertados correctamente")
            else:
                print("ℹ️  La base de datos ya contiene datos")
                
    except Exception as e:
        print(f"❌ Error al inicializar la base de datos: {e}")

if __name__ == '__main__':
    print("🚀 Inicializando base de datos MySQL...")
    
    if create_database():
        init_database()
        print("✅ Proceso completado exitosamente")
    else:
        print("❌ Error en el proceso de inicialización")
