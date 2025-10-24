from typing import List, Optional, Dict, Any
from app.repositories.profesor_repository import ProfesorRepository
from app.models.profesor import Profesor

class ProfesorService:
    """Service class for Profesor business logic"""
    
    @staticmethod
    def create_profesor(profesor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new profesor with validation"""
        try:
            # Validate required fields
            required_fields = ['nombre', 'apellido', 'dni', 'email']
            for field in required_fields:
                if not profesor_data.get(field):
                    return {'error': f'Campo {field} es requerido', 'status': 400}
            
            # Check if email already exists
            existing_profesor = ProfesorRepository.get_by_email(profesor_data['email'])
            if existing_profesor:
                return {'error': 'El email ya está en uso', 'status': 409}
            
            # Check if DNI already exists
            existing_dni = ProfesorRepository.get_by_dni(profesor_data['dni'])
            if existing_dni:
                return {'error': 'El DNI ya está registrado', 'status': 409}
            
            profesor = ProfesorRepository.create(profesor_data)
            return {'data': profesor.to_dict(), 'status': 201}
            
        except Exception as e:
            return {'error': f'Error al crear profesor: {str(e)}', 'status': 500}
    
    @staticmethod
    def get_profesor(profesor_id: int) -> Dict[str, Any]:
        """Get profesor by ID"""
        try:
            profesor = ProfesorRepository.get_by_id(profesor_id)
            if not profesor:
                return {'error': 'Profesor no encontrado', 'status': 404}
            return {'data': profesor.to_dict(), 'status': 200}
        except Exception as e:
            return {'error': f'Error al obtener profesor: {str(e)}', 'status': 500}
    
    @staticmethod
    def get_all_profesores() -> Dict[str, Any]:
        """Get all profesores"""
        try:
            profesores = ProfesorRepository.get_all()
            return {'data': [profesor.to_dict() for profesor in profesores], 'status': 200}
        except Exception as e:
            return {'error': f'Error al obtener profesores: {str(e)}', 'status': 500}
    
    @staticmethod
    def get_active_profesores() -> Dict[str, Any]:
        """Get active profesores"""
        try:
            profesores = ProfesorRepository.get_active()
            return {'data': [profesor.to_dict() for profesor in profesores], 'status': 200}
        except Exception as e:
            return {'error': f'Error al obtener profesores activos: {str(e)}', 'status': 500}
    
    @staticmethod
    def update_profesor(profesor_id: int, profesor_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update profesor"""
        try:
            profesor = ProfesorRepository.get_by_id(profesor_id)
            if not profesor:
                return {'error': 'Profesor no encontrado', 'status': 404}
            
            # Check email uniqueness if email is being updated
            if 'email' in profesor_data and profesor_data['email'] != profesor.email:
                existing_profesor = ProfesorRepository.get_by_email(profesor_data['email'])
                if existing_profesor:
                    return {'error': 'El email ya está en uso', 'status': 409}
            
            # Check DNI uniqueness if DNI is being updated
            if 'dni' in profesor_data and profesor_data['dni'] != profesor.dni:
                existing_dni = ProfesorRepository.get_by_dni(profesor_data['dni'])
                if existing_dni:
                    return {'error': 'El DNI ya está registrado', 'status': 409}
            
            updated_profesor = ProfesorRepository.update(profesor_id, profesor_data)
            return {'data': updated_profesor.to_dict(), 'status': 200}
            
        except Exception as e:
            return {'error': f'Error al actualizar profesor: {str(e)}', 'status': 500}
    
    @staticmethod
    def delete_profesor(profesor_id: int) -> Dict[str, Any]:
        """Delete profesor (soft delete)"""
        try:
            profesor = ProfesorRepository.get_by_id(profesor_id)
            if not profesor:
                return {'error': 'Profesor no encontrado', 'status': 404}
            
            ProfesorRepository.soft_delete(profesor_id)
            return {'message': 'Profesor eliminado exitosamente', 'status': 200}
            
        except Exception as e:
            return {'error': f'Error al eliminar profesor: {str(e)}', 'status': 500}
    
    @staticmethod
    def get_profesores_by_especialidad(especialidad: str) -> Dict[str, Any]:
        """Get profesores by especialidad"""
        try:
            profesores = ProfesorRepository.get_by_especialidad(especialidad)
            return {'data': [profesor.to_dict() for profesor in profesores], 'status': 200}
        except Exception as e:
            return {'error': f'Error al obtener profesores por especialidad: {str(e)}', 'status': 500}
