from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.delivery import Delivery, DeliveryStatus, Exception
from app.models.order import Order
from app.models.user import DelivererProfile

class DeliveryService:
    def assign_delivery(self, db: Session, order_id: int, deliverer_id: int):
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise ValueError("订单不存在")
        
        delivery = Delivery(
            order_id=order_id,
            deliverer_id=deliverer_id,
            status=DeliveryStatus.ASSIGNED
        )
        db.add(delivery)
        
        order.status = "delivering"
        db.commit()
        db.refresh(delivery)
        return delivery
    
    def start_delivery(self, db: Session, delivery_id: int):
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        if delivery and delivery.status == DeliveryStatus.ASSIGNED:
            delivery.status = DeliveryStatus.IN_TRANSIT
            db.commit()
            db.refresh(delivery)
            return delivery
        return None
    
    def complete_delivery(self, db: Session, delivery_id: int):
        delivery = db.query(Delivery).filter(Delivery.id == delivery_id).first()
        # 允许完成ASSIGNED和IN_TRANSIT状态的配送
        if delivery and delivery.status in [DeliveryStatus.ASSIGNED, DeliveryStatus.IN_TRANSIT]:
            delivery.status = DeliveryStatus.DELIVERED
            delivery.actual_time = datetime.utcnow()
            delivery.end_time = datetime.utcnow()
            
            order = db.query(Order).filter(Order.id == delivery.order_id).first()
            if order:
                order.status = "completed"
            
            db.commit()
            db.refresh(delivery)
            return delivery
        return None
    
    def update_deliverer_location(self, db: Session, deliverer_id: int, latitude: str, longitude: str):
        """更新配送员位置（直接更新 deliverer_profiles 表）"""
        profile = db.query(DelivererProfile).filter(DelivererProfile.user_id == deliverer_id).first()
        if profile:
            profile.latitude = latitude
            profile.longitude = longitude
            profile.location_updated_at = datetime.utcnow()
            db.commit()
            db.refresh(profile)
            return {
                "user_id": profile.user_id,
                "latitude": profile.latitude,
                "longitude": profile.longitude,
                "location_updated_at": profile.location_updated_at
            }
        return None
    
    def get_deliverer_location(self, db: Session, deliverer_id: int):
        """获取配送员位置（从 deliverer_profiles 表）"""
        profile = db.query(DelivererProfile).filter(DelivererProfile.user_id == deliverer_id).first()
        if profile and profile.latitude and profile.longitude:
            return {
                "user_id": profile.user_id,
                "latitude": profile.latitude,
                "longitude": profile.longitude,
                "timestamp": profile.location_updated_at
            }
        return None
    
    def get_deliverer_deliveries(self, db: Session, deliverer_id: int, status: Optional[str] = None):
        query = db.query(Delivery).filter(Delivery.deliverer_id == deliverer_id)
        if status:
            query = query.filter(Delivery.status == status)
        return query.order_by(Delivery.created_at.desc()).all()
    
    def report_exception(self, db: Session, delivery_id: int, exception_type: str, description: str):
        exception = Exception(
            delivery_id=delivery_id,
            type=exception_type,
            description=description
        )
        db.add(exception)
        db.commit()
        db.refresh(exception)
        return exception
    
    def get_delivery(self, db: Session, delivery_id: int):
        return db.query(Delivery).filter(Delivery.id == delivery_id).first()

delivery_service = DeliveryService()
