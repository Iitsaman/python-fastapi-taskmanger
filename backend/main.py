from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import engine, Base
from app.routes import auth, tasks
from app.admin import create_admin_if_not_exists
import logging

from prometheus_fastapi_instrumentator import Instrumentator

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="Async Task Manager API")


# React frontend CORS
origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers with API versioning
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])

# Root endpoint for health check
@app.get("/")
async def root():
    return {"message": "API is running", "version": "v1.0"}

# startup event
@app.on_event("startup")
async def startup_event():
    # Create DB tables asynchronously
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables created")

    # Create admin user if not exists (async)
    await create_admin_if_not_exists()
    logging.info("Admin check completed")


# Prometheus  Instrumentation
#instrumentator = Instrumentator()
instrumentator = Instrumentator(
    should_group_status_codes=True,  
    excluded_handlers=["/metrics"]   
)
instrumentator.instrument(app).expose(app, endpoint="/metrics")





# myenv\Scripts\activate

#  uvicorn main:app --reload


 