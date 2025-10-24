from datetime import datetime
from app.models.database import db

class Profesor(db.Model):
    __tablename__ = 'profesor'
    
    profesor_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    dni = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    especialidad = db.Column(db.String(100), nullable=True)
    titulo_academico = db.Column(db.String(100), nullable=True)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    
    def __repr__(self):
        return f'<Profesor {self.nombre} {self.apellido}>'
    
    def to_dict(self):
        return {
            'profesor_id': self.profesor_id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'dni': self.dni,
            'email': self.email,
            'telefono': self.telefono,
            'especialidad': self.especialidad,
            'titulo_academico': self.titulo_academico,
            'fecha_registro': self.fecha_registro.isoformat() if self.fecha_registro else None,
            'activo': self.activo
        }
