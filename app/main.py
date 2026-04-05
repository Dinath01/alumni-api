from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.models.profile import Profile
from app.models.bid import Bid

from app.routes.auth_routes import router as auth_router
from app.routes.profile_routes import router as profile_router

from app.routes.bid_routes import router as bid_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(bid_router)

@app.get("/")
def root():
    return {"message": "API is running"}