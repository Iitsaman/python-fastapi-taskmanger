from pydantic import BaseModel
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = ""

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

    class Config:
        orm_mode = True