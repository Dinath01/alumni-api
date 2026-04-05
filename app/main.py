from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import Base, engine
from app.models.user import User
from app.models.profile import Profile
from app.models.bid import Bid
from app.models.featured_alumnis import FeaturedAlumnis

from app.routes.featured_routes import router as featured_router
from app.routes.bid_routes import router as bid_router
from app.routes.auth_routes import router as auth_router
from app.routes.profile_routes import router as profile_router

from app.services.schedular_services import start_scheduler

Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield

app = FastAPI(
    title="Alumni Influencer API",
    description="Backend API for alumni profiles",
    version="1.0.1",
    lifespan=lifespan,
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(profile_router)
app.include_router(bid_router)
app.include_router(featured_router)

@app.get("/")
def root():
    return {"message": "API is running"}