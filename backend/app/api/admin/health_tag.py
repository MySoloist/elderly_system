from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.health_tag import HealthTag
from app.schemas.health_tag import HealthTag as HealthTagSchema, HealthTagCreate, HealthTagUpdate

router = APIRouter()

@router.get("/health-tags", response_model=List[HealthTagSchema])
def get_health_tags(db: Session = Depends(get_db)):
    """获取所有健康标签"""
    tags = db.query(HealthTag).all()
    return tags

@router.post("/health-tags", response_model=HealthTagSchema)
def create_health_tag(tag: HealthTagCreate, db: Session = Depends(get_db)):
    """创建健康标签"""
    # 检查标签名称是否已存在
    existing_tag = db.query(HealthTag).filter(HealthTag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="健康标签名称已存在")
    
    db_tag = HealthTag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.get("/health-tags/{tag_id}", response_model=HealthTagSchema)
def get_health_tag(tag_id: int, db: Session = Depends(get_db)):
    """获取单个健康标签"""
    tag = db.query(HealthTag).filter(HealthTag.id == tag_id).first()
    if tag is None:
        raise HTTPException(status_code=404, detail="健康标签不存在")
    return tag

@router.put("/health-tags/{tag_id}", response_model=HealthTagSchema)
def update_health_tag(tag_id: int, tag: HealthTagUpdate, db: Session = Depends(get_db)):
    """更新健康标签"""
    db_tag = db.query(HealthTag).filter(HealthTag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="健康标签不存在")
    
    # 检查新名称是否与其他标签重复
    if tag.name and tag.name != db_tag.name:
        existing_tag = db.query(HealthTag).filter(HealthTag.name == tag.name).first()
        if existing_tag:
            raise HTTPException(status_code=400, detail="健康标签名称已存在")
    
    update_data = tag.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tag, field, value)
    
    db.commit()
    db.refresh(db_tag)
    return db_tag

@router.delete("/health-tags/{tag_id}")
def delete_health_tag(tag_id: int, db: Session = Depends(get_db)):
    """删除健康标签"""
    db_tag = db.query(HealthTag).filter(HealthTag.id == tag_id).first()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="健康标签不存在")
    
    db.delete(db_tag)
    db.commit()
    return {"message": "健康标签删除成功"}
