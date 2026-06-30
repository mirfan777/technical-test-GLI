from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db
from app.api.routes.tasks import router as tasks_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def test_ping():
    return {"message": "FastAPI stands ready!"}

app.include_router(tasks_router, prefix="/tasks", tags=["tasks"])