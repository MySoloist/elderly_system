from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.models.order import Order, OrderItem
from app.models.meal import Meal
from app.models.delivery import Delivery, DeliveryStatus

class OrderService:
    def create_order(self, db: Session, user_id: int, items: List[dict], delivery_address: str, 
                    notes: Optional[str] = None, scheduled_time: Optional[datetime] = None,
                    order_type: str = "immediate"):
        total_amount = 0.0
        order_items = []
        
        for item_data in items:
            meal = db.query(Meal).filter(Meal.id == item_data['meal_id']).first()
            if not meal or meal.status != 'available':
                raise ValueError(f"餐品 {item_data['meal_id']} 不可用")
            
            item = OrderItem(
                meal_id=meal.id,
                quantity=item_data['quantity'],
                unit_price=meal.price,
                subtotal=meal.price * item_data['quantity']
            )
            order_items.append(item)
            total_amount += meal.price * item_data['quantity']
        
        # 所有订单都先进入待支付状态
        status = "pending_payment"
        
        order = Order(
            elderly_id=user_id,
            total_amount=total_amount,
            delivery_address=delivery_address,
            notes=notes,
            scheduled_time=scheduled_time,
            order_type=order_type,
            status=status
        )
        db.add(order)
        db.flush()
        
        for item in order_items:
            item.order_id = order.id
            db.add(item)
        
        db.commit()
        db.refresh(order)
        return order
    
    def get_user_orders(self, db: Session, user_id: int, status: Optional[str] = None, 
                       skip: int = 0, limit: int = 20):
        query = db.query(Order).filter(Order.elderly_id == user_id)
        if status:
            query = query.filter(Order.status == status)
        return query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_order(self, db: Session, order_id: int):
        return db.query(Order).filter(Order.id == order_id).first()
    
    def update_order_status(self, db: Session, order_id: int, status: str):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.status = status
            db.commit()
            db.refresh(order)
        return order
    
    def cancel_order(self, db: Session, order_id: int):
        order = db.query(Order).filter(Order.id == order_id).first()
        if order and order.status in ["pending_payment", "pending_schedule", "pending_accept"]:
            order.status = "cancelled"
            db.commit()
            db.refresh(order)
            return order
        return None
    
    def get_available_orders(self, db: Session, skip: int = 0, limit: int = 20):
        return db.query(Order).filter(Order.status == "pending_accept").offset(skip).limit(limit).all()

order_service = OrderService()