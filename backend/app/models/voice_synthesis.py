from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Float
from sqlalchemy.orm import relationship
from app.core.database import Base


class VoiceSynthesis(Base):
    __tablename__ = "voice_synthesis"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    text_content = Column(Text, nullable=False)
    voice_url = Column(String(500), nullable=True)
    voice_type = Column(String(50), nullable=True)  # 语音类型，如：female, male, elderly
    language = Column(String(20), nullable=True, default="zh_CN")
    speed = Column(Float, nullable=True, default=0.8)
    status = Column(String(20), nullable=True, default="pending")  # pending, processing, completed, failed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    user = relationship("User", backref="voice_syntheses")