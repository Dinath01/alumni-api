from pydantic import BaseModel, Field
from decimal import Decimal


class BidCreate(BaseModel):
    amount: Decimal = Field(gt=0)


class BidResponse(BaseModel):
    id: int
    user_id: int
    amount: Decimal
    is_winner: bool

    class Config:
        from_attributes = True

#win or lose
class BidStatusResponse(BaseModel):
    status: str  