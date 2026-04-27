from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import User, ElderlyProfile, MemberProfile, DelivererProfile, AdminProfile, Review
from app.core.security import get_password_hash

class UserService:
    def create_user(self, db: Session, username: str, password: str, user_type: str, openid: str = None, unionid: str = None):
        hashed_password = get_password_hash(password)
        user = User(
            username=username,
            password_hash=hashed_password,
            user_type=user_type,
            openid=openid,
            unionid=unionid,
            status="active"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_username(self, db: Session, username: str):
        return db.query(User).filter(User.username == username).first()
    
    def get_user_by_id(self, db: Session, user_id: int):
        return db.query(User).filter(User.id == user_id).first()
    
    def update_user_profile(self, db: Session, user: User, profile_data: dict):
        if user.user_type == "elderly":
            if not user.elderly_profile:
                user.elderly_profile = ElderlyProfile()
            for key, value in profile_data.items():
                setattr(user.elderly_profile, key, value)
        elif user.user_type == "member":
            if not user.member_profile:
                user.member_profile = MemberProfile()
            for key, value in profile_data.items():
                setattr(user.member_profile, key, value)
        elif user.user_type == "deliverer":
            if not user.deliverer_profile:
                user.deliverer_profile = DelivererProfile()
            for key, value in profile_data.items():
                setattr(user.deliverer_profile, key, value)
        elif user.user_type == "admin":
            if not user.admin_profile:
                user.admin_profile = AdminProfile()
            for key, value in profile_data.items():
                setattr(user.admin_profile, key, value)
        
        db.commit()
        db.refresh(user)
        return user
    
    def get_deliverer_average_rating(self, db: Session, deliverer_id: int):
        """计算配送员的平均评分"""
        result = db.query(func.avg(Review.rating)).filter(
            Review.deliverer_id == deliverer_id,
            Review.status == "approved"
        ).scalar()
        
        return round(float(result), 1) if result else 0.0

user_service = UserService()