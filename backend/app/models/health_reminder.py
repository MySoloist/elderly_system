from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func

from app.core.database import Base


class HealthReminder(Base):
    __tablename__ = "health_reminders"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    reminder_type = Column(String(50), nullable=False)  # diet, health, checkup
    content = Column(Text, nullable=False)
    status = Column(String(20), default="pending")  # pending, sent, read
    scheduled_time = Column(DateTime(timezone=True))
    sent_time = Column(DateTime(timezone=True))
    read_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
