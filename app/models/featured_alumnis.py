from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.database import Base


class FeaturedAlumnis(Base):
    __tablename__ = "featured_alumni"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    winning_bid = Column(Numeric(10, 2), nullable=False)
    feature_date = Column(Date, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")