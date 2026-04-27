from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class HealthRecord(Base):
    __tablename__ = "health_records"
    
    id = Column(Integer, primary_key=True, index=True)
    elderly_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    height = Column(Float, nullable=True)
    weight = Column(Float, nullable=True)
    blood_pressure = Column(String(20), nullable=True)
    blood_sugar = Column(Float, nullable=True)
    allergies = Column(Text, nullable=True)
    medications = Column(Text, nullable=True)
    doctor_advice = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    # 关系
    elderly = relationship("User", foreign_keys=[elderly_id], backref="health_records")
    creator = relationship("User", foreign_keys=[created_by])
