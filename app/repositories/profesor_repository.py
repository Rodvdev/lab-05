from typing import List, Optional
from app.models.profesor import Profesor
from app.models.database import db

class ProfesorRepository:
    """Repository class for Profesor model operations"""
    
    @staticmethod
    def create(profesor_data: dict) -> Profesor:
        """Create a new profesor"""
        profesor = Profesor(
            nombre=profesor_data['nombre'],
            apellido=profesor_data['apellido'],
            dni=profesor_data['dni'],
            email=profesor_data['email'],
            telefono=profesor_data.get('telefono'),
            especialidad=profesor_data.get('especialidad'),
            titulo_academico=profesor_data.get('titulo_academico'),
            activo=profesor_data.get('activo', True)
        )
        db.session.add(profesor)
        db.session.commit()
        return profesor
    
    @staticmethod
    def get_by_id(profesor_id: int) -> Optional[Profesor]:
        """Get profesor by ID"""
        return Profesor.query.get(profesor_id)
    
    @staticmethod
    def get_by_email(email: str) -> Optional[Profesor]:
        """Get profesor by email"""
        return Profesor.query.filter_by(email=email).first()
    
    @staticmethod
    def get_by_dni(dni: str) -> Optional[Profesor]:
        """Get profesor by DNI"""
        return Profesor.query.filter_by(dni=dni).first()
    
    @staticmethod
    def get_all() -> List[Profesor]:
        """Get all profesores"""
        return Profesor.query.all()
    
    @staticmethod
    def get_active() -> List[Profesor]:
        """Get all active profesores"""
        return Profesor.query.filter_by(activo=True).all()
    
    @staticmethod
    def get_by_especialidad(especialidad: str) -> List[Profesor]:
        """Get profesores by especialidad"""
        return Profesor.query.filter_by(especialidad=especialidad).all()
    
    @staticmethod
    def update(profesor_id: int, profesor_data: dict) -> Optional[Profesor]:
        """Update profesor"""
        profesor = ProfesorRepository.get_by_id(profesor_id)
        if profesor:
            for key, value in profesor_data.items():
                if hasattr(profesor, key):
                    setattr(profesor, key, value)
            db.session.commit()
        return profesor
    
    @staticmethod
    def delete(profesor_id: int) -> bool:
        """Delete profesor"""
        profesor = ProfesorRepository.get_by_id(profesor_id)
        if profesor:
            db.session.delete(profesor)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def soft_delete(profesor_id: int) -> bool:
        """Soft delete profesor (set activo to False)"""
        profesor = ProfesorRepository.get_by_id(profesor_id)
        if profesor:
            profesor.activo = False
            db.session.commit()
            return True
        return False
