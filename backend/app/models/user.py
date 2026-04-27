from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from app.core.database import Base
from app.models.community import Community
from app.models.health_tag import HealthTag

class UserType(str, enum.Enum):
    elderly = "elderly"
    member = "member"
    deliverer = "deliverer"
    admin = "admin"

class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    openid = Column(String(100), unique=True)
    unionid = Column(String(100), unique=True)
    user_type = Column(Enum(UserType), nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.ACTIVE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    elderly_profile = relationship("ElderlyProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    member_profile = relationship("MemberProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    deliverer_profile = relationship("DelivererProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin_profile = relationship("AdminProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")

class ElderlyProfile(Base):
    __tablename__ = "elderly_profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    community_id = Column(Integer, ForeignKey("communities.id"))
    health_tag_id = Column(Integer, ForeignKey("health_tags.id"))
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True)
    address = Column(String(255))
    dietary_preferences = Column(String(255))
    location = Column(String(255), nullable=True)
    age = Column(Integer)
    gender = Column(String(10))
    avatar = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="elderly_profile")
    community = relationship("Community", back_populates="elderly_profiles")
    health_tag = relationship("HealthTag", backref="elderly_profiles")

class MemberProfile(Base):
    __tablename__ = "member_profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True)
    avatar = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="member_profile")

class DelivererProfile(Base):
    __tablename__ = "deliverer_profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    area_id = Column(Integer, ForeignKey("delivery_areas.id"))
    name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True)
    vehicle_type = Column(String(50))
    status = Column(String(20), default="offline")
    avatar = Column(String(255))
    # 位置信息字段（从 deliverer_locations 表合并）
    latitude = Column(String(20))
    longitude = Column(String(20))
    location_updated_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="deliverer_profile")
    area = relationship("DeliveryArea", back_populates="deliverer_profiles")

class AdminProfile(Base):
    __tablename__ = "admin_profiles"
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    name = Column(String(50), nullable=False)
    phone = Column(String(20))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    user = relationship("User", back_populates="admin_profile")


class DeliveryArea(Base):
    __tablename__ = "delivery_areas"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    deliverer_profiles = relationship("DelivererProfile", back_populates="area")