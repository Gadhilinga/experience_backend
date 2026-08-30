from fastapi import FastAPI
from core.database import Base, engine
from models.saved_destination import SavedDestination
from models.user import User

from routers.auth import router as auth_router
from routers.explore import router as explore_router

app = FastAPI(
    title="Experience Backend API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(explore_router)


@app.on_event("startup")
def create_database_tables():
    Base.metadata.create_all(bind=engine)
