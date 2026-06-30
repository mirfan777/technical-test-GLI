from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

class TaskRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Task]:
        statement = select(Task)
        return list(self.session.scalars(statement).all())

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.session.get(Task, task_id)

    def create(self, task_data: TaskCreate) -> Task:
        db_task = Task(**task_data.model_dump())
        self.session.add(db_task)
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def update(self, db_task: Task, task_data: TaskUpdate) -> Task:
        obj_data = task_data.model_dump(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_task, key, value)
            
        self.session.commit()
        self.session.refresh(db_task)
        return db_task

    def delete(self, db_task: Task) -> None:
        self.session.delete(db_task)
        self.session.commit()