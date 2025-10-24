from typing import List, Optional
from models.task import Task
from models.database import db

class TaskRepository:
    """Repository class for Task model operations"""
    
    @staticmethod
    def create(task_data: dict) -> Task:
        """Create a new task"""
        task = Task(
            title=task_data['title'],
            description=task_data.get('description'),
            user_id=task_data['user_id']
        )
        db.session.add(task)
        db.session.commit()
        return task
    
    @staticmethod
    def get_by_id(task_id: int) -> Optional[Task]:
        """Get task by ID"""
        return Task.query.get(task_id)
    
    @staticmethod
    def get_by_user_id(user_id: int) -> List[Task]:
        """Get all tasks for a user"""
        return Task.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_all() -> List[Task]:
        """Get all tasks"""
        return Task.query.all()
    
    @staticmethod
    def update(task_id: int, task_data: dict) -> Optional[Task]:
        """Update task"""
        task = TaskRepository.get_by_id(task_id)
        if task:
            for key, value in task_data.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            db.session.commit()
        return task
    
    @staticmethod
    def delete(task_id: int) -> bool:
        """Delete task"""
        task = TaskRepository.get_by_id(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def mark_completed(task_id: int) -> Optional[Task]:
        """Mark task as completed"""
        return TaskRepository.update(task_id, {'completed': True})
    
    @staticmethod
    def mark_pending(task_id: int) -> Optional[Task]:
        """Mark task as pending"""
        return TaskRepository.update(task_id, {'completed': False})
