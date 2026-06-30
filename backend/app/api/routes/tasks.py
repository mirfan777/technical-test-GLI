from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import get_db  
from app.schemas.task import TaskResponse, TaskCreate, TaskUpdate
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

router = APIRouter()

def get_task_service(session: Session = Depends(get_db)) -> TaskService:
    repository = TaskRepository(session)
    return TaskService(repository)

@router.get("/", response_model=List[TaskResponse])
def read_all_tasks(service: TaskService = Depends(get_task_service)):
    return service.get_tasks()

@router.post("/", response_model=TaskResponse)
def create_new_task(
    task_in: TaskCreate, 
    service: TaskService = Depends(get_task_service)
):
    return service.create_task(task_in)

@router.patch("/{task_id}", response_model=TaskResponse)
def update_existing_task(
    task_id: int, 
    task_in: TaskUpdate, 
    service: TaskService = Depends(get_task_service)
):
    return service.update_task_status(task_id, task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_task(
    task_id: int,
    service: TaskService = Depends(get_task_service)
):
    service.delete_task(task_id)