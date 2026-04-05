from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.schemas.bid_schemas import BidCreate, BidStatusResponse
from app.services.auth_service import get_current_user
from app.services.bid_service import place_bid, get_bid_status

router = APIRouter(prefix="/bids", tags=["Bidding"])


@router.post("/")
def place_my_bid(
    bid: BidCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    new_bid = place_bid(db, current_user.id, bid.amount)

    if not new_bid:
        raise HTTPException(
            status_code=400,
            detail="The bid must be higher than your current bid"
        )

    return {"message": "Bid placed successfully"}


@router.get("/status", response_model=BidStatusResponse)
def get_my_status(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    status = get_bid_status(db, current_user.id)

    if not status:
        raise HTTPException(status_code=404, detail="No bid found")

    return {"status": status}