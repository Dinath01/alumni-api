from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import extract, func

from app.models.bid import Bid
from app.models.featured_alumnis import FeaturedAlumnis


def count_user_wins_this_month(db: Session, user_id: int, target_date: date):
    return (
        db.query(func.count(FeaturedAlumnis.id))
        .filter(FeaturedAlumnis.user_id == user_id)
        .filter(extract("year", FeaturedAlumnis.feature_date) == target_date.year)
        .filter(extract("month", FeaturedAlumnis.feature_date) == target_date.month)
        .scalar()
    )


def select_daily_winner(db: Session, target_date: date):
    existing_feature = (
        db.query(FeaturedAlumnis)
        .filter(FeaturedAlumnis.feature_date == target_date)
        .first()
    )

    if existing_feature:
        return existing_feature

    all_bids = db.query(Bid).order_by(Bid.amount.desc()).all()

    for bid in all_bids:
        win_count = count_user_wins_this_month(db, bid.user_id, target_date)

        if win_count < 3:
            feature = FeaturedAlumnis(
                user_id=bid.user_id,
                winning_bid=bid.amount,
                feature_date=target_date
            )

            bid.is_winner = True

            db.add(feature)
            db.commit()
            db.refresh(feature)

            return feature

    return None


def get_featured_alumnis_by_date(db: Session, target_date: date):
    return (
        db.query(FeaturedAlumnis)
        .filter(FeaturedAlumnis.feature_date == target_date)
        .first()
    )


def get_today_featured_alumnis(db: Session):
    return get_featured_alumnis_by_date(db, date.today())