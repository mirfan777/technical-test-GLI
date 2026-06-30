from typing import List
from fastapi import HTTPException, status
from app.repositories.task_repository import TaskRepository
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def get_tasks(self) -> List[Task]:
        return self.repository.get_all()

    def create_task(self, task_data: TaskCreate) -> Task:
        # Contoh validasi bisnis: Judul task tidak boleh kosong/spasi doang
        if not task_data.title.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Judul task tidak boleh kosong"
            )
        return self.repository.create(task_data)

    def update_task_status(self, task_id: int, task_data: TaskUpdate) -> Task:
        # Cek apakah task-nya ada atau tidak
        db_task = self.repository.get_by_id(task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task tidak ditemukan"
            )
            
        # Contoh logika bisnis: Validasi status yang diperbolehkan
        if task_data.status and task_data.status not in ["Todo", "In Progress", "Done"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Status harus berupa: Todo, In Progress, atau Done"
            )
            
        return self.repository.update(db_task, task_data)

    def delete_task(self, task_id: int) -> None:
        db_task = self.repository.get_by_id(task_id)
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task tidak ditemukan"
            )
        self.repository.delete(db_task)