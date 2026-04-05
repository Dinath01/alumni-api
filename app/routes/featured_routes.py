from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.featured_schema import FeaturedAlumnisResponse
from app.services.featured_service import (
    select_daily_winner,
    get_today_featured_alumnis,
)

router = APIRouter(prefix="/featured", tags=["Featured Alumnus"])


@router.post("/select-winner", response_model=FeaturedAlumnisResponse)
def select_winner(db: Session = Depends(get_db)):
    feature = select_daily_winner(db, date.today())

    if not feature:
        raise HTTPException(status_code=404, detail="No eligible bids found")

    return feature


@router.get("/today", response_model=FeaturedAlumnisResponse)
def get_today_featured(db: Session = Depends(get_db)):
    feature = get_today_featured_alumnis(db)

    if not feature:
        raise HTTPException(status_code=404, detail="No featured alumnus for today")

    return feature