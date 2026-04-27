from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.community import Community


class CommunityService:
    def get_communities(self, db: Session, skip: int = 0, limit: int = 20):
        """获取社区列表"""
        return db.query(Community).offset(skip).limit(limit).all()
    
    def get_community(self, db: Session, community_id: int):
        """获取单个社区信息"""
        return db.query(Community).filter(Community.id == community_id).first()
    
    def create_community(self, db: Session, name: str, address: Optional[str] = None,
                        contact_phone: Optional[str] = None, manager_name: Optional[str] = None,
                        manager_phone: Optional[str] = None, status: str = "正常"):
        """创建社区"""
        community = Community(
            name=name,
            address=address,
            contact_phone=contact_phone,
            manager_name=manager_name,
            manager_phone=manager_phone,
            status=status
        )
        db.add(community)
        db.commit()
        db.refresh(community)
        return community
    
    def update_community(self, db: Session, community_id: int, **kwargs):
        """更新社区信息"""
        community = db.query(Community).filter(Community.id == community_id).first()
        if community:
            # 移除elderly_count字段，使用实时查询
            kwargs.pop('elderly_count', None)
            for key, value in kwargs.items():
                setattr(community, key, value)
            db.commit()
            db.refresh(community)
        return community
    
    def delete_community(self, db: Session, community_id: int):
        """删除社区"""
        community = db.query(Community).filter(Community.id == community_id).first()
        if community:
            db.delete(community)
            db.commit()
            return True
        return False


community_service = CommunityService()
