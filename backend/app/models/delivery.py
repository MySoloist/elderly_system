from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

class DeliveryStatus(str, enum.Enum):
    ASSIGNED = "assigned"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
    FAILED = "failed"

class Delivery(Base):
    __tablename__ = "deliveries"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    deliverer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(Enum(DeliveryStatus), default=DeliveryStatus.ASSIGNED)
    estimated_time = Column(DateTime(timezone=True))
    actual_time = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_assigned_by_admin = Column(Boolean, default=False)
    end_time = Column(DateTime(timezone=True))
    
    order = relationship("Order", back_populates="delivery")
    deliverer = relationship("User")
    exceptions = relationship("Exception", back_populates="delivery", cascade="all, delete-orphan")



class Exception(Base):
    __tablename__ = "exceptions"
    id = Column(Integer, primary_key=True, index=True)
    delivery_id = Column(Integer, ForeignKey("deliveries.id"), nullable=False)
    type = Column(String(50), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    delivery = relationship("Delivery", back_populates="exceptions")