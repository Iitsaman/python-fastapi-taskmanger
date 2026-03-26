from fastapi import FastAPI
from app.db import engine, Base
from app.models import user, tasks
from app.routes import auth, tasks
from fastapi.middleware.cors import CORSMiddleware

from app.admin import create_admin_if_not_exists

app = FastAPI(title="Task Manager API")

# React frontend

origins = [
    "http://localhost:5173",  
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 

# routers with API versioning
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])

# Create DB tables
Base.metadata.create_all(bind=engine)

# Root endpoint for health check
@app.get("/")
def root():
    return {"message": "API is running", "version": "v1.0"}

@app.on_event("startup")
def startup_event():
    create_admin_if_not_exists()








