from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.announcement import Announcement


class AnnouncementService:
    def get_announcements(self, db: Session, skip: int = 0, limit: int = 20):
        """获取通知列表"""
        return db.query(Announcement).offset(skip).limit(limit).all()
    
    def get_announcement(self, db: Session, announcement_id: int):
        """获取单个通知详情"""
        return db.query(Announcement).filter(Announcement.id == announcement_id).first()
    
    def create_announcement(self, db: Session, title: str, content: str, 
                          announcement_type: str, priority: str = "normal", status: str = "active"):
        """创建通知"""
        announcement = Announcement(
            title=title,
            content=content,
            type=announcement_type,
            priority=priority,
            status=status
        )
        db.add(announcement)
        db.commit()
        db.refresh(announcement)
        return announcement
    
    def update_announcement(self, db: Session, announcement_id: int, **kwargs):
        """更新通知"""
        announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
        if announcement:
            for key, value in kwargs.items():
                setattr(announcement, key, value)
            db.commit()
            db.refresh(announcement)
        return announcement
    
    def delete_announcement(self, db: Session, announcement_id: int):
        """删除通知"""
        announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
        if announcement:
            db.delete(announcement)
            db.commit()
            return True
        return False


announcement_service = AnnouncementService()
