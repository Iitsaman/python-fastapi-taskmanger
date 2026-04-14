from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db import get_db
from app.models.tasks import Task
from app.schema.tasks import TaskCreate, TaskUpdate, TaskResponse

from app.routes.auth import get_current_user, require_role

from app.metrics import tasks_created, failed_requests ,tasks_updated, tasks_deleted 

import logging

router = APIRouter(tags=["Tasks"])


# Create Task

@router.post("/", response_model=TaskResponse)
async def create_task(
    task: TaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Create a new task
        new_task = Task(
            title=task.title,
            description=task.description,
            owner_id=current_user.id
        )
        db.add(new_task)
        await db.commit()
        await db.refresh(new_task)

        # Increment Prometheus counter
        tasks_created.inc()

        return new_task


    except Exception as e:
        failed_requests.inc()
        raise HTTPException(status_code=500, detail="Internal server error") from e

# List Own Tasks
@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Task).filter(Task.owner_id == current_user.id))
    tasks = result.scalars().all()
    return tasks


# Admin-only List All Tasks
@router.get("/all", response_model=List[TaskResponse])
async def list_all_tasks(
    db: AsyncSession = Depends(get_db),
    admin_user=Depends(require_role("admin"))
):
    result = await db.execute(select(Task))
    tasks = result.scalars().all()
    return tasks


# Get Single Task
@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    result = await db.execute(select(Task).filter(Task.id == task_id))
    task = result.scalars().first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.owner_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Forbidden")
    return task


# Update Task
@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Fetch task
        result = await db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            failed_requests.inc()
            raise HTTPException(status_code=404, detail="Task not found")

        # Check ownership / admin rights
        if task.owner_id != current_user.id and current_user.role != "admin":
            failed_requests.inc()
            raise HTTPException(status_code=403, detail="Forbidden")

        # Update fields if provided
        if task_update.title is not None:
            task.title = task_update.title
        if task_update.description is not None:
            task.description = task_update.description
        if task_update.completed is not None:
            task.completed = task_update.completed

        await db.commit()
        await db.refresh(task)

        # Increment Prometheus counter
        tasks_updated.inc()

        return task

    except HTTPException:
        
        raise
    except Exception as e:
        failed_requests.inc()
        logging.error(f"Failed to update task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e



# Delete Task

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        # Fetch the task
        result = await db.execute(select(Task).filter(Task.id == task_id))
        task = result.scalars().first()
        if not task:
            failed_requests.inc()
            raise HTTPException(status_code=404, detail="Task not found")

        # Check ownership / admin rights
        if task.owner_id != current_user.id and current_user.role != "admin":
            failed_requests.inc()
            raise HTTPException(status_code=403, detail="Forbidden")

        # Delete the task
        await db.delete(task)
        await db.commit()

        # Increment Prometheus counter
        tasks_deleted.inc()

        return {"message": "Task deleted successfully"}

    except HTTPException:
        # Already counted failed_requests for 404/403 above
        raise
    except Exception as e:
        failed_requests.inc()
        logging.error(f"Failed to delete task {task_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error") from e