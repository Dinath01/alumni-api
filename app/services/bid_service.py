from sqlalchemy.orm import Session
from app.models.bid import Bid


def place_bid(db: Session, user_id: int, amount):
    #already bid checking
    existing_bid = db.query(Bid).filter(Bid.user_id == user_id).first()

    if existing_bid:
        
        if amount <= existing_bid.amount:
            return None

        existing_bid.amount = amount
        db.commit()
        db.refresh(existing_bid)
        return existing_bid

    #new bid creation
    new_bid = Bid(user_id=user_id, amount=amount)
    db.add(new_bid)
    db.commit()
    db.refresh(new_bid)

    return new_bid


def get_bid_status(db: Session, user_id: int):
    user_bid = db.query(Bid).filter(Bid.user_id == user_id).first()

    if not user_bid:
        return None

    highest_bid = db.query(Bid).order_by(Bid.amount.desc()).first()

    if user_bid.id == highest_bid.id:
        return "winning"

    return "losing"