from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.mongodb import create_indexes
from app.routes import plants, users

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plants.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_event():
    # Create unique indexes in MongoDB
    await create_indexes()

@app.get("/")
def root():
    return {"message": "Potato Planting Pirates API 🏴‍☠️"}
