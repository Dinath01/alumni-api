from datetime import date
from decimal import Decimal
from pydantic import BaseModel


class FeaturedAlumnisResponse(BaseModel):
    user_id: int
    winning_bid: Decimal
    feature_date: date

    class Config:
        from_attributes = True