from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    

app = FastAPI()

@app.get("/")
def test_ping():
    return {"message": "FastAPI stands ready!"}