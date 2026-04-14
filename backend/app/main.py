from fastapi import FastAPI
from app.config.mongodb import create_indexes
from app.routes import plants, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.include_router(plants.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    # Create unique indexes in MongoDB
    await create_indexes()

app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")