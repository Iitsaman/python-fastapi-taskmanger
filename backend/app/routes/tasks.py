from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.db import SessionLocal
from app.models.tasks import Task
from app.schema.tasks import TaskCreate, TaskUpdate, TaskResponse
from app.utils.dependencies import get_current_user, require_role, get_db
from app.routes.auth import get_current_user, require_role  

router = APIRouter( tags=["Tasks"])


#  Database Dependency 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#  Create Task 
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    new_task = Task(
        title=task.title,
        description=task.description,
        owner_id=current_user.id
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


#  List Own Tasks 
@router.get("/", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    return tasks


#  Admin-only List All Tasks 
@router.get("/all", response_model=List[TaskResponse])
def list_all_tasks(db: Session = Depends(get_db), admin_user=Depends(require_role("admin"))):
    tasks = db.query(Task).all()
    return tasks


#  Get Single Task 
@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return task


#  Update Task 
@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    if task_update.title is not None:
        task.title = task_update.title
    if task_update.description is not None:
        task.description = task_update.description
    if task_update.completed is not None:
        task.completed = task_update.completed

    db.commit()
    db.refresh(task)
    return task



#  Delete Task 
@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")

    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

