from datetime import datetime
from models.database import db

class Profesor(db.Model):
    __tablename__ = 'profesores'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    apellido = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    especialidad = db.Column(db.String(100), nullable=False)
    salario = db.Column(db.Numeric(10, 2), nullable=False)
    fecha_contratacion = db.Column(db.Date, nullable=False)
    activo = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Profesor {self.nombre} {self.apellido}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'telefono': self.telefono,
            'especialidad': self.especialidad,
            'salario': float(self.salario) if self.salario else None,
            'fecha_contratacion': self.fecha_contratacion.isoformat() if self.fecha_contratacion else None,
            'activo': self.activo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
