from .database import Base
from sqlalchemy import Column, DateTime, Integer, String, Boolean, func
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    rating = Column(Integer, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)