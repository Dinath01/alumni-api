from fastapi import FastAPI

from app.db.database import Base, engine
from app.models.user import User
from app.models.profile import Profile
from app.models.bid import Bid

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {"message": "API is running"}