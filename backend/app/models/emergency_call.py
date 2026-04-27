from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class EmergencyCall(Base):
    __tablename__ = "emergency_calls"

    id = Column(Integer, primary_key=True, index=True)
    elderly_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    emergency_type = Column(String(50), nullable=False)  # medical, fire, police, other, family_call, family_sms
    message = Column(Text)
    response_status = Column(String(20), default="pending")
    response_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
