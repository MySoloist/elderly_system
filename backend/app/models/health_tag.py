from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class HealthTag(Base):
    __tablename__ = "health_tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    color = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
