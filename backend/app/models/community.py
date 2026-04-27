from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Community(Base):
    __tablename__ = "communities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255))
    contact_phone = Column(String(20))
    manager_name = Column(String(50))
    manager_phone = Column(String(20))
    status = Column(String(20), default="正常")  # 正常、暂停服务
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    elderly_profiles = relationship("ElderlyProfile", back_populates="community")
