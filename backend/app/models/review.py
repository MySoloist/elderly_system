from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Review(Base):
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=True)
    elderly_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer)
    content = Column(Text)
    status = Column(String(20), default="approved")
    images = Column(ARRAY(Text), nullable=True)
    reply = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True))
    ai_reviewed = Column(Integer, default=0)  # 0: 人工审核, 1: AI审核
    ai_replied = Column(Integer, default=0)  # 0: 人工回复, 1: AI回复
    deliverer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    reviewer_type = Column(String(20), nullable=False, default="elderly")
    
    # 关系
    elderly = relationship("User", backref="reviews", foreign_keys=[elderly_id])
    order = relationship("Order", backref="review")
    deliverer = relationship("User", backref="deliverer_reviews", foreign_keys=[deliverer_id])
