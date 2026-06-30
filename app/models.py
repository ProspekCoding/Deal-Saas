from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from app.database import Base


class ProductPrice(Base):
    __tablename__ = "product_prices"

    id = Column(Integer, primary_key=True, index=True)
    product_key = Column(String, index=True)
    brand = Column(String)

    name = Column(String)
    price = Column(Float)
    old_price = Column(Float, nullable=True)

    timestamp = Column(DateTime, default=datetime.utcnow)