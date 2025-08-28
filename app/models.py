from sqlalchemy import Column, Integer, String, Float, Boolean
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    balance = Column(Float, default=0.0)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    service_id = Column(Integer)
    link = Column(String)
    quantity = Column(Integer)
    status = Column(String, default="pending")

class Topup(Base):
    __tablename__ = "topups"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    amount = Column(Float)
    approved = Column(Boolean, default=False)
