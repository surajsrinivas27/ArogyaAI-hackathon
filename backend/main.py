from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth import router as auth_router

from app.database import connect_to_mongo, close_mongo_connection
from app.routers import family
from app.routers import reports
@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    await close_mongo_connection()


app = FastAPI(
    title="ArogyaAI API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(family.router)
app.include_router(reports.router)
@app.get("/")
async def root():
    return {
        "message": "Welcome to ArogyaAI API",
        "status": "running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }