from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_tables
from routes.reviews import router as reviews_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    print("Database tables created")
    yield
#     shutdown : cleanup here
    print("Shutting down the app ")

app = FastAPI(
    title="Cineplax Review API",
    version="1.0",
    description="Theater Reviews Api for Cineplax",
    lifespan=lifespan
)
app.include_router(reviews_router)
@app.get("/")
async def root():
    return {"message": "Welcome to CinePlax Review Api"}