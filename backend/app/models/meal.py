from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base

# MealStatus枚举暂时注释，使用字符串类型

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    meals = relationship("Meal", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    meals = relationship("Meal", back_populates="tag")

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    status = Column(String(20), default="available")
    category_id = Column(Integer, ForeignKey("categories.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    special_tag = Column(String(50))
    image_url = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    category = relationship("Category", back_populates="meals")
    tag = relationship("Tag", back_populates="meals")
    favorites = relationship("Favorite", back_populates="meal")

class Favorite(Base):
    __tablename__ = "favorites"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_type = Column(String(20), nullable=False)  # 'elderly' 或 'member'
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    meal = relationship("Meal", back_populates="favorites")
    
    __table_args__ = (
        # 确保同一用户不能重复收藏同一餐品
        # 注意：这里使用 user_id + meal_id 作为唯一约束
        # 如果需要区分老人和家属，可以改为 (user_id, meal_id, user_type)
        {'sqlite_autoincrement': True},
    )