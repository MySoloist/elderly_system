from sqlalchemy import Column, Integer, String, Date, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.database import Base

class StaffSchedule(Base):
    __tablename__ = "staff_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    staff_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    schedule_date = Column(Date, nullable=False)
    time_slot = Column(String(20), nullable=False)  # 如 '08:00-10:00'
    status = Column(String(20), default="confirmed")  # confirmed, pending, cancelled
    note = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # 关系
    staff = relationship("User", backref="schedules")
