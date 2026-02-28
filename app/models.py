from sqlalchemy import Column, String, Boolean, BigInteger, TIMESTAMP, Integer
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    is_deleted = Column(Boolean, nullable=False, default=False)

class Watermark(Base):
    __tablename__ = "watermarks"
    id = Column(Integer, primary_key=True, index=True)
    consumer_id = Column(String(255), nullable=False, unique=True)
    last_exported_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)