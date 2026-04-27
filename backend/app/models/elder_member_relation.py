from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship as sa_relationship

from app.core.database import Base


class ElderMemberRelation(Base):
    """老人家属绑定关系模型"""
    __tablename__ = "elder_member_relations"
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    elder_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    relationship = Column(String(50), nullable=False)
    is_primary = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系定义
    member = sa_relationship("User", foreign_keys=[member_id], backref="member_relations")
    elder = sa_relationship("User", foreign_keys=[elder_id], backref="elder_relations")
