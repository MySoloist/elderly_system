from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from pydantic import BaseModel
from sqlalchemy import text, func
import json
from datetime import datetime
import os
import uuid

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User, UserType, ElderlyProfile
from app.models.elder_member_relation import ElderMemberRelation
from app.models.meal import Category
from app.models.order import Order, Payment, OrderItem
from app.models.health_record import HealthRecord
from app.models.announcement import Announcement
from app.models.health_reminder import HealthReminder
from app.models.review import Review
from app.services.order_service import order_service
from app.services.announcement_service import announcement_service
from app.services.meal_service import meal_service
from app.services.health_advice_service import HealthAdviceService

router = APIRouter(prefix="/member", tags=["家属端"])

class ElderlyInfo(BaseModel):
    id: int
    name: str
    phone: str
    relationship: str
    health_status: Optional[str] = None
    dietary_preferences: Optional[str] = None
    
    class Config:
        from_attributes = True

class BindElderly(BaseModel):
    elder_id: int
    relationship: str

class OrderItemCreate(BaseModel):
    meal_id: int
    quantity: int

class OrderCreate(BaseModel):
    elder_id: int
    items: List[OrderItemCreate]
    delivery_address: str
    special_notes: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    order_type: str = "immediate"

class PaymentRequest(BaseModel):
    payment_method: str

class HealthReminderCreate(BaseModel):
    receiver_id: int
    reminder_type: str
    content: str
    scheduled_time: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    order_no: str
    elderly_name: str
    total_amount: float
    status: str
    delivery_time: str
    created_at: str
    
    class Config:
        from_attributes = True

@router.get("/elders", response_model=List[ElderlyInfo])
def get_elders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 这里应该实现获取绑定老人的逻辑
    # 暂时返回模拟数据
    return [
        ElderlyInfo(
            id=1,
            name="张奶奶",
            phone="138****5678",
            relationship="母亲",
            health_status="健康",
            dietary_preferences="低糖"
        )
    ]

@router.post("/elders")
def bind_elderly(
    bind_data: BindElderly,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 这里应该实现绑定老人的逻辑
    # 暂时返回模拟数据
    return {
        "id": 1,
        "elder_id": bind_data.elder_id,
        "member_id": current_user.id,
        "relationship": bind_data.relationship,
        "is_primary": False
    }

@router.get("/orders", response_model=dict)
def get_orders(
    elder_id: Optional[int] = Query(None, description="老人ID"),
    status: Optional[str] = Query(None, description="订单状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取老人订单列表"""
    skip = (page - 1) * limit
    
    # 查询订单
    orders = order_service.get_user_orders(db, elder_id, status=status, skip=skip, limit=limit)
    
    # 查询总数
    total_query = db.query(Order).filter(Order.elderly_id == elder_id)
    if status:
        total_query = total_query.filter(Order.status == status)
    total = total_query.count()
    
    # 构造响应数据
    items = []
    for order in orders:
        # 获取订单商品信息
        order_items = []
        for item in order.items:
            order_items.append({
                "meal": {
                    "id": item.meal.id,
                    "name": item.meal.name,
                    "price": item.meal.price,
                    "image_url": item.meal.image_url
                },
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            })
        
        items.append({
            "id": order.id,
            "elderly_id": order.elderly_id,
            "total_amount": order.total_amount,
            "status": order.status,
            "order_type": order.order_type,
            "scheduled_time": order.scheduled_time.isoformat() if order.scheduled_time else None,
            "delivery_address": order.delivery_address,
            "notes": order.notes,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
            "paid_at": order.payment.created_at.isoformat() if order.payment else None,
            "items": order_items
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/orders/{order_id}", response_model=dict)
def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单详情"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 获取老人信息
    elderly = db.query(ElderlyProfile).filter(ElderlyProfile.user_id == order.elderly_id).first()
    
    # 构造响应数据
    order_items = []
    for item in order.items:
        order_items.append({
            "meal": {
                "id": item.meal.id,
                "name": item.meal.name,
                "price": item.meal.price,
                "image_url": item.meal.image_url
            },
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal
        })
    
    # 获取配送员信息
    delivery_man = None
    delivery_phone = None
    estimated_time = None
    
    if order.delivery and order.delivery.deliverer:
        deliverer_profile = order.delivery.deliverer.deliverer_profile
        if deliverer_profile:
            delivery_man = deliverer_profile.name
            delivery_phone = deliverer_profile.phone
        estimated_time = order.delivery.estimated_time
    
    return {
        "id": order.id,
        "elderly_id": order.elderly_id,
        "elderly_name": elderly.name if elderly else "未知老人",
        "total_amount": order.total_amount,
        "status": order.status,
        "order_type": order.order_type,
        "scheduled_time": order.scheduled_time.isoformat() if order.scheduled_time else None,
        "delivery_address": order.delivery_address,
        "notes": order.notes,
        "payment_method": order.payment.payment_method if order.payment else None,
        "delivery_man": delivery_man,
        "delivery_phone": delivery_phone,
        "estimated_time": estimated_time.isoformat() if estimated_time else None,
        "created_at": order.created_at.isoformat(),
        "updated_at": order.updated_at.isoformat(),
        "paid_at": order.payment.created_at.isoformat() if order.payment else None,
        "items": order_items
    }


@router.post("/orders")
def create_order_for_elder(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        items = [item.dict() for item in order_data.items]
        order = order_service.create_order(
            db,
            user_id=order_data.elder_id,
            items=items,
            delivery_address=order_data.delivery_address,
            notes=order_data.special_notes,
            scheduled_time=order_data.scheduled_time,
            order_type=order_data.order_type
        )
        return {
            "id": order.id,
            "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:03d}",
            "elderly_id": order.elderly_id,
            "member_id": current_user.id,
            "total_amount": order.total_amount,
            "status": order.status
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/orders/{order_id}/pay")
def pay_order(
    order_id: int,
    payment_data: PaymentRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """支付订单"""
    # 获取订单
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 验证订单状态
    if order.status != "pending_payment":
        raise HTTPException(status_code=400, detail="订单状态不允许支付")
    
    # 创建支付记录
    payment = Payment(
        order_id=order.id,
        payment_method=payment_data.payment_method,
        amount=order.total_amount,
        status="paid",
        transaction_id=f"TXN{datetime.now().strftime('%Y%m%d%H%M%S')}{order.id}"
    )
    
    # 根据订单类型设置不同的状态
    if order.order_type == "scheduled":
        order.status = "pending_schedule"
    else:
        order.status = "pending_accept"
    
    db.add(payment)
    db.commit()
    db.refresh(order)
    
    return {
        "id": order.id,
        "status": order.status,
        "payment_method": payment.payment_method,
        "payment_status": payment.status,
        "transaction_id": payment.transaction_id
    }

@router.post("/orders/{order_id}/cancel")
def cancel_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消订单"""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 验证订单是否属于该家属绑定的老人
    relation = db.query(ElderMemberRelation).filter(
        ElderMemberRelation.member_id == current_user.id,
        ElderMemberRelation.elder_id == order.elderly_id
    ).first()
    
    if not relation:
        raise HTTPException(status_code=403, detail="无权操作此订单")
    
    cancelled_order = order_service.cancel_order(db, order_id)
    if not cancelled_order:
        raise HTTPException(status_code=400, detail="只能取消待支付或等待预定时间的订单")
    
    return {"message": "订单取消成功", "order_id": order_id, "status": "cancelled"}


@router.get("/orders/{order_id}/track")
def track_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 这里应该实现跟踪订单的逻辑
    # 暂时返回模拟数据
    return {
        "order_id": order_id,
        "status": "delivering",
        "estimated_time": "2024-01-15T12:30:00",
        "deliverer": {
            "name": "李师傅",
            "phone": "139****9012",
            "current_location": {
                "latitude": 39.9042,
                "longitude": 116.4074
            },
            "distance": "1.2km",
            "estimated_arrival": "12:25"
        },
        "elderly_location": {
            "latitude": 39.9142,
            "longitude": 116.4174
        }
    }

@router.get("/health/{elder_id}")
def get_elder_health(
    elder_id: int,
    date: Optional[str] = Query(None, description="查询日期，格式：YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 验证家属是否有权限查看该老人的健康记录
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": elder_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权查看该老人的健康记录")
    
    # 获取老人健康记录
    health_records = db.query(HealthRecord).filter(HealthRecord.elderly_id == elder_id).order_by(HealthRecord.recorded_at.desc()).limit(10).all()
    
    # 获取老人基本信息
    elderly = db.query(User).filter(User.id == elder_id).first()
    
    if not elderly:
        raise HTTPException(status_code=404, detail="老人不存在")
    
    # 获取老人的订单数据，用于计算营养摄入
    query = db.query(Order).filter(Order.elderly_id == elder_id, Order.status == "completed")
    
    # 根据日期筛选订单
    if date:
        # 筛选指定日期的订单
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        query = query.filter(func.date(Order.created_at) == target_date)
    else:
        # 默认筛选今天的订单
        query = query.filter(func.date(Order.created_at) == func.current_date())
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    # 计算营养摄入
    total_calories = 0
    total_protein = 0
    total_fat = 0
    total_carbs = 0
    
    for order in orders:
        for item in order.items:
            # 使用真实的special_tag数据
            calories = item.meal.price * 10  # 简化计算
            protein = calories * 0.15
            fat = calories * 0.25
            carbs = calories * 0.6
            
            total_calories += calories
            total_protein += protein
            total_fat += fat
            total_carbs += carbs
    
    # 准备健康数据响应
    health_data = {
        "elder_id": elder_id,
        "elder_name": elderly.username,
        "health_status": elderly.elderly_profile.health_tag.name if elderly.elderly_profile and elderly.elderly_profile.health_tag else "正常",
        "health_tags": [],  # 可以从健康记录中提取
        "nutrition": {
            "calories": round(total_calories),
            "protein": round(total_protein),
            "fat": round(total_fat),
            "carbs": round(total_carbs)
        },
        "diet_pattern": {
            "breakfast": {"time": "", "has_meal": False},
            "lunch": {"time": "", "has_meal": False},
            "dinner": {"time": "", "has_meal": False}
        },
        "diet_regularity": "良好",
        "diet_records": []
    }
    
    # 从订单数据构建饮食记录和饮食规律
    for order in orders:
        order_date = order.created_at.strftime("%Y-%m-%d")
        order_time = order.created_at.strftime("%H:%M")
        
        # 判断是早餐、午餐还是晚餐
        hour = order.created_at.hour
        
        if hour < 11:
            meal_type = "早餐"
            health_data["diet_pattern"]["breakfast"]["time"] = order_time
            health_data["diet_pattern"]["breakfast"]["has_meal"] = True
        elif hour < 17:
            meal_type = "午餐"
            health_data["diet_pattern"]["lunch"]["time"] = order_time
            health_data["diet_pattern"]["lunch"]["has_meal"] = True
        else:
            meal_type = "晚餐"
            health_data["diet_pattern"]["dinner"]["time"] = order_time
            health_data["diet_pattern"]["dinner"]["has_meal"] = True
        
        foods = []
        order_calories = 0
        
        for item in order.items:
            food_calories = item.meal.price * 10  # 简化计算
            order_calories += food_calories
            
            foods.append({
                "name": item.meal.name,
                "calories": round(food_calories),
                "image": item.meal.image_url
            })
        
        # 收集该订单中所有餐品的special_tag
        nutrition_tags = set()
        for item in order.items:
            if item.meal.special_tag:
                nutrition_tags.add(item.meal.special_tag)
        
        health_data["diet_records"].append({
            "time": order_time,
            "meal": meal_type,
            "foods": foods,
            "totalCalories": round(order_calories),
            "nutritionTags": list(nutrition_tags) if nutrition_tags else ["蛋白质", "碳水"]
        })
    
    # 根据饮食规律判断饮食规律状态
    meals_count = sum(1 for meal in health_data["diet_pattern"].values() if meal["has_meal"])
    if meals_count >= 2:
        health_data["diet_regularity"] = "良好"
    elif meals_count == 1:
        health_data["diet_regularity"] = "一般"
    else:
        health_data["diet_regularity"] = "不规律"
    
    return health_data

class HealthRecordCreate(BaseModel):
    elderly_id: int
    blood_pressure: Optional[str] = None
    blood_sugar: Optional[float] = None
    weight: Optional[float] = None
    temperature: Optional[float] = None
    heart_rate: Optional[int] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


@router.post("/health")
def add_health_record(
    health_data: HealthRecordCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加老人健康记录"""
    # 验证家属是否有权限为该老人添加健康记录
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": health_data.elderly_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权为该老人添加健康记录")
    
    # 创建健康记录，将体温和心率存储在doctor_advice字段中
    doctor_advice = []
    if health_data.temperature:
        doctor_advice.append(f"体温: {health_data.temperature}°C")
    if health_data.heart_rate:
        doctor_advice.append(f"心率: {health_data.heart_rate}次/分钟")
    if health_data.notes:
        doctor_advice.append(f"备注: {health_data.notes}")
    if health_data.tags:
        doctor_advice.append(f"健康标签: {', '.join(health_data.tags)}")
    
    doctor_advice_text = "\n".join(doctor_advice) if doctor_advice else None
    
    health_record = HealthRecord(
        elderly_id=health_data.elderly_id,
        blood_pressure=health_data.blood_pressure,
        blood_sugar=health_data.blood_sugar,
        weight=health_data.weight,
        doctor_advice=doctor_advice_text,
        created_by=current_user.id
    )
    
    db.add(health_record)
    db.commit()
    db.refresh(health_record)
    
    return {
        "id": health_record.id,
        "elderly_id": health_record.elderly_id,
        "blood_pressure": health_record.blood_pressure,
        "blood_sugar": health_record.blood_sugar,
        "weight": health_record.weight,
        "doctor_advice": health_record.doctor_advice,
        "created_at": health_record.recorded_at.isoformat()
    }


# 口味偏好相关API
class TastePreferences(BaseModel):
    tastes: List[str]
    allergies: List[str]
    special_needs: Optional[str] = None


@router.get("/elderly/{elder_id}/preferences")
def get_elderly_preferences(
    elder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取老人口味偏好"""
    # 验证家属是否有权限查看该老人的偏好
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": elder_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权查看该老人的偏好")
    
    # 获取老人档案信息
    elderly_profile = db.execute(
        text("SELECT dietary_preferences FROM elderly_profiles WHERE user_id = :user_id"),
        {"user_id": elder_id}
    ).fetchone()
    
    if not elderly_profile:
        raise HTTPException(status_code=404, detail="老人档案不存在")
    
    # 解析口味偏好数据
    dietary_preferences = elderly_profile.dietary_preferences
    tastes = []
    allergies = []
    special_needs = ""
    
    if dietary_preferences:
        try:
            data = json.loads(dietary_preferences)
            tastes = data.get("tastes", [])
            allergies = data.get("allergies", [])
            special_needs = data.get("special_needs", "")
        except json.JSONDecodeError:
            pass
    
    # 获取老人基本信息
    elderly = db.query(User).filter(User.id == elder_id).first()
    
    return {
        "elder_id": elder_id,
        "elder_name": elderly.username,
        "tastes": tastes,
        "allergies": allergies,
        "special_needs": special_needs
    }


@router.post("/elderly/{elder_id}/preferences")
def update_elderly_preferences(
    elder_id: int,
    preferences: TastePreferences,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新老人口味偏好"""
    # 验证家属是否有权限更新该老人的偏好
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": elder_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权更新该老人的偏好")
    
    # 获取老人档案信息
    elderly_profile = db.execute(
        text("SELECT user_id FROM elderly_profiles WHERE user_id = :user_id"),
        {"user_id": elder_id}
    ).fetchone()
    
    if not elderly_profile:
        raise HTTPException(status_code=404, detail="老人档案不存在")
    
    # 将口味偏好数据转换为JSON格式
    dietary_preferences = json.dumps({
        "tastes": preferences.tastes,
        "allergies": preferences.allergies,
        "special_needs": preferences.special_needs
    })
    
    # 更新数据库中的口味偏好字段
    db.execute(
        text("""
            UPDATE elderly_profiles 
            SET dietary_preferences = :dietary_preferences, 
                updated_at = NOW() 
            WHERE user_id = :user_id
        """),
        {"dietary_preferences": dietary_preferences, "user_id": elder_id}
    )
    db.commit()
    
    # 获取老人基本信息
    elderly = db.query(User).filter(User.id == elder_id).first()
    
    return {
        "elder_id": elder_id,
        "elder_name": elderly.username,
        "tastes": preferences.tastes,
        "allergies": preferences.allergies,
        "special_needs": preferences.special_needs,
        "updated_at": datetime.now().isoformat()
    }


@router.get("/consume/{elder_id}")
def get_elder_consume(
    elder_id: int,
    date: Optional[str] = Query(None, description="查询日期，格式：YYYY-MM-DD"),
    start_date: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 获取老人的订单数据，用于计算消费统计
    query = db.query(Order).filter(Order.elderly_id == elder_id, Order.status == "completed")
    
    # 根据日期筛选订单
    if date:
        # 筛选指定日期的订单
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
        query = query.filter(func.date(Order.created_at) == target_date)
    elif start_date and end_date:
        # 筛选日期范围的订单
        start = datetime.strptime(start_date, "%Y-%m-%d").date()
        end = datetime.strptime(end_date, "%Y-%m-%d").date()
        query = query.filter(func.date(Order.created_at) >= start, func.date(Order.created_at) <= end)
    else:
        # 默认筛选本月的订单
        today = datetime.now().date()
        month_start = datetime(today.year, today.month, 1).date()
        query = query.filter(func.date(Order.created_at) >= month_start)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    # 计算消费统计
    total_amount = sum(order.total_amount for order in orders)
    order_count = len(orders)
    avg_amount = total_amount / order_count if order_count > 0 else 0
    
    # 计算环比数据（简化计算，实际应该对比上个月）
    amount_trend = 12  # 简化计算
    order_trend = 8    # 简化计算
    avg_trend = 5      # 简化计算
    
    # 构建账单分组
    bill_groups = {}
    for order in orders:
        order_date = order.created_at.strftime("%Y-%m-%d")
        order_time = order.created_at.strftime("%H:%M")
        
        # 判断是早餐、午餐还是晚餐
        hour = order.created_at.hour
        meal_type = "早餐" if hour < 11 else "午餐" if hour < 17 else "晚餐"
        
        if order_date not in bill_groups:
            bill_groups[order_date] = []
        
        bill_groups[order_date].append({
            "name": meal_type,
            "time": order_time,
            "amount": order.total_amount
        })
    
    # 转换为前端需要的格式
    bill_groups_list = []
    for date_str, bills in sorted(bill_groups.items(), reverse=True):
        bill_groups_list.append({
            "date": date_str,
            "bills": bills
        })
    
    return {
        "total_amount": round(total_amount, 2),
        "order_count": order_count,
        "avg_amount": round(avg_amount, 2),
        "amount_trend": amount_trend,
        "order_trend": order_trend,
        "avg_trend": avg_trend,
        "bill_groups": bill_groups_list
    }

# 绑定管理API端点
class BindingCreate(BaseModel):
    elderly_id: int
    relation: str

class BindingUpdate(BaseModel):
    relation: str

class BindingResponse(BaseModel):
    id: int
    elderly_id: int
    elderly_name: str
    elderly_age: Optional[int] = None
    elderly_gender: Optional[str] = None
    elderly_address: Optional[str] = None
    relation: str
    
    class Config:
        from_attributes = True

@router.get("/bindings", response_model=List[BindingResponse])
def get_bindings(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取家属绑定的老人列表"""
    query = text("""
        SELECT 
            emr.id,
            emr.elder_id as elderly_id,
            ep.name as elderly_name,
            ep.age as elderly_age,
            ep.gender as elderly_gender,
            ep.address as elderly_address,
            emr.relationship as relation
        FROM elder_member_relations emr
        JOIN users u ON emr.elder_id = u.id
        JOIN elderly_profiles ep ON u.id = ep.user_id
        WHERE emr.member_id = :member_id
        ORDER BY emr.created_at DESC
    """)
    result = db.execute(query, {"member_id": current_user.id}).fetchall()
    
    return [
        BindingResponse(
            id=row.id,
            elderly_id=row.elderly_id,
            elderly_name=row.elderly_name,
            elderly_age=row.elderly_age,
            elderly_gender=row.elderly_gender,
            elderly_address=row.elderly_address,
            relation=row.relation
        )
        for row in result
    ]

@router.post("/bindings", response_model=BindingResponse)
def create_binding(
    binding_data: BindingCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加老人绑定"""
    # 检查老人是否存在
    elder_query = text("""
        SELECT 
            u.id,
            ep.name,
            ep.age,
            ep.gender
        FROM users u
        JOIN elderly_profiles ep ON u.id = ep.user_id
        WHERE u.id = :elder_id AND u.user_type = 'elderly'
    """)
    elder = db.execute(elder_query, {"elder_id": binding_data.elderly_id}).fetchone()
    
    if not elder:
        raise HTTPException(status_code=404, detail="老人不存在")
    
    # 检查是否已经绑定
    existing = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": binding_data.elderly_id, "member_id": current_user.id}
    ).fetchone()
    
    if existing:
        raise HTTPException(status_code=400, detail="该老人已经绑定")
    
    # 创建绑定
    query = text("""
        INSERT INTO elder_member_relations (elder_id, member_id, relationship)
        VALUES (:elder_id, :member_id, :relationship)
        RETURNING id
    """)
    result = db.execute(query, {
        "elder_id": binding_data.elderly_id,
        "member_id": current_user.id,
        "relationship": binding_data.relation
    }).fetchone()
    
    db.commit()
    
    return BindingResponse(
        id=result.id,
        elderly_id=binding_data.elderly_id,
        elderly_name=elder.name,
        elderly_age=elder.age,
        elderly_gender=elder.gender,
        relation=binding_data.relation
    )

@router.get("/bindings/{elder_id}", response_model=BindingResponse)
def get_binding(
    elder_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取绑定详情"""
    query = text("""
        SELECT 
            emr.id,
            emr.elder_id as elderly_id,
            ep.name as elderly_name,
            ep.age as elderly_age,
            ep.gender as elderly_gender,
            emr.relationship as relation
        FROM elder_member_relations emr
        JOIN users u ON emr.elder_id = u.id
        JOIN elderly_profiles ep ON u.id = ep.user_id
        WHERE emr.elder_id = :elder_id AND emr.member_id = :member_id
    """)
    result = db.execute(query, {"elder_id": elder_id, "member_id": current_user.id}).fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="绑定不存在")
    
    return BindingResponse(
        id=result.id,
        elderly_id=result.elderly_id,
        elderly_name=result.elderly_name,
        elderly_age=result.elderly_age,
        elderly_gender=result.elderly_gender,
        relation=result.relation
    )

@router.put("/bindings/{binding_id}", response_model=BindingResponse)
def update_binding(
    binding_id: int,
    binding_data: BindingUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新绑定信息"""
    # 检查绑定是否存在且属于当前用户
    existing = db.execute(
        text("SELECT id FROM elder_member_relations WHERE id = :binding_id AND member_id = :member_id"),
        {"binding_id": binding_id, "member_id": current_user.id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(status_code=404, detail="绑定不存在")
    
    # 更新绑定
    query = text("""
        UPDATE elder_member_relations 
        SET relationship = :relationship, updated_at = NOW()
        WHERE id = :binding_id
        RETURNING elder_id
    """)
    result = db.execute(query, {
        "binding_id": binding_id,
        "relationship": binding_data.relation
    }).fetchone()
    
    db.commit()
    
    # 获取更新后的完整信息
    binding = get_binding(binding_id, current_user, db)
    return binding

@router.delete("/bindings/{binding_id}")
def delete_binding(
    binding_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除绑定"""
    # 检查绑定是否存在且属于当前用户
    existing = db.execute(
        text("SELECT id FROM elder_member_relations WHERE id = :binding_id AND member_id = :member_id"),
        {"binding_id": binding_id, "member_id": current_user.id}
    ).fetchone()
    
    if not existing:
        raise HTTPException(status_code=404, detail="绑定不存在")
    
    # 删除绑定
    db.execute(
        text("DELETE FROM elder_member_relations WHERE id = :binding_id"),
        {"binding_id": binding_id}
    )
    db.commit()
    
    return {"message": "绑定已删除"}

@router.get("/elderly-list")
def get_elderly_list(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取可绑定的老人列表"""
    query = text("""
        SELECT 
            u.id,
            ep.name,
            ep.phone,
            ep.age,
            ep.gender
        FROM users u
        JOIN elderly_profiles ep ON u.id = ep.user_id
        WHERE u.user_type = 'elderly'
        AND u.id NOT IN (
            SELECT elder_id FROM elder_member_relations WHERE member_id = :member_id
        )
        ORDER BY ep.name
    """)
    result = db.execute(query, {"member_id": current_user.id}).fetchall()
    
    return [
        {
            "id": row.id,
            "name": row.name,
            "phone": row.phone,
            "age": row.age,
            "gender": row.gender
        }
        for row in result
    ]


@router.get("/categories", response_model=dict)
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有分类列表"""
    categories = db.query(Category).all()
    
    return {
        "categories": [
            {
                "id": category.id,
                "name": category.name,
                "description": category.description
            }
            for category in categories
        ]
    }


@router.get("/announcements", response_model=dict)
def get_announcements(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取公告列表"""
    skip = (page - 1) * limit
    # 只获取已发布的公告（status='active'），不显示草稿
    announcements = db.query(Announcement).filter(Announcement.status == "active").offset(skip).limit(limit).all()
    
    # 获取已发布公告的总数
    total = db.query(Announcement).filter(Announcement.status == "active").count()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": [
            {
                "id": announcement.id,
                "title": announcement.title,
                "content": announcement.content,
                "type": announcement.type,
                "priority": announcement.priority,
                "status": announcement.status,
                "created_at": announcement.created_at,
                "updated_at": announcement.updated_at
            }
            for announcement in announcements
        ]
    }

@router.get("/elderly-emergency-calls")
def get_elderly_emergency_calls(
    elderly_id: int = Query(..., description="老人ID"),
    emergency_type: Optional[str] = Query(None, description="紧急类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取老人的紧急呼叫记录"""
    from app.models.emergency_call import EmergencyCall
    
    # 验证家属是否有权限查看该老人的记录
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": elderly_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权访问该老人的记录")
    
    # 查询紧急呼叫记录
    query = db.query(EmergencyCall).filter(EmergencyCall.elderly_id == elderly_id)
    
    if emergency_type:
        query = query.filter(EmergencyCall.emergency_type == emergency_type)
    
    # 按时间倒序排列
    calls = query.order_by(EmergencyCall.created_at.desc()).limit(20).all()
    
    return [
        {
            "id": call.id,
            "elderly_id": call.elderly_id,
            "emergency_type": call.emergency_type,
            "message": call.message,
            "response_status": call.response_status,
            "response_time": call.response_time.isoformat() if call.response_time else None,
            "created_at": call.created_at.isoformat()
        }
        for call in calls
    ]


@router.post("/health-reminders")
def create_health_reminder(
    reminder_data: HealthReminderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """发送健康提醒给老人"""
    # 验证家属是否有权限发送提醒给该老人
    binding = db.execute(
        text("SELECT id FROM elder_member_relations WHERE elder_id = :elder_id AND member_id = :member_id"),
        {"elder_id": reminder_data.receiver_id, "member_id": current_user.id}
    ).fetchone()
    
    if not binding:
        raise HTTPException(status_code=403, detail="无权向该老人发送提醒")
    
    # 创建健康提醒记录
    scheduled_datetime = None
    if reminder_data.scheduled_time:
        try:
            scheduled_datetime = datetime.strptime(reminder_data.scheduled_time, "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            raise HTTPException(status_code=400, detail="时间格式错误，应为YYYY-MM-DDTHH:MM:SS")
    
    reminder = HealthReminder(
        sender_id=current_user.id,
        receiver_id=reminder_data.receiver_id,
        reminder_type=reminder_data.reminder_type,
        content=reminder_data.content,
        scheduled_time=scheduled_datetime,
        status="pending"
    )
    
    db.add(reminder)
    db.commit()
    db.refresh(reminder)
    
    return {
        "id": reminder.id,
        "sender_id": reminder.sender_id,
        "receiver_id": reminder.receiver_id,
        "reminder_type": reminder.reminder_type,
        "content": reminder.content,
        "status": reminder.status,
        "scheduled_time": reminder.scheduled_time.isoformat() if reminder.scheduled_time else None,
        "created_at": reminder.created_at.isoformat()
    }


# 家属收藏餐品相关API
class FavoriteMemberCreate(BaseModel):
    meal_id: int


@router.post("/favorites")
def add_member_favorite(
    favorite_data: FavoriteMemberCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """添加餐品到收藏"""
    try:
        favorite = meal_service.add_favorite(db, current_user.id, "member", favorite_data.meal_id)
        return {
            "id": favorite.id,
            "meal_id": favorite.meal_id,
            "created_at": favorite.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"添加收藏失败: {str(e)}")


@router.get("/favorites", response_model=dict)
def get_member_favorites(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取收藏餐品列表"""
    favorites = meal_service.get_user_favorites(db, current_user.id, "member")
    
    items = []
    for fav in favorites:
        items.append({
            "id": fav.meal.id,
            "name": fav.meal.name,
            "price": fav.meal.price,
            "image_url": fav.meal.image_url,
            "category": fav.meal.category.name if fav.meal.category else "",
            "special_tag": fav.meal.special_tag
        })
    
    return {
        "total": len(favorites),
        "items": items
    }


@router.delete("/favorites/{meal_id}")
def remove_member_favorite(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """从收藏中移除餐品"""
    success = meal_service.remove_favorite(db, current_user.id, "member", meal_id)
    if success:
        return {"message": "收藏已移除"}
    raise HTTPException(status_code=404, detail="收藏不存在")


@router.get("/health-advice/{elderly_id}")
async def get_health_advice(
    elderly_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取老人的AI健康建议"""
    try:
        advice = await HealthAdviceService.get_health_advice(db, elderly_id)
        return {"advice": advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail="获取健康建议失败")


@router.get("/reviews")
def get_member_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取家属绑定老人的评价列表"""
    # 获取家属绑定的所有老人ID
    bind_relations = db.query(ElderMemberRelation).filter(
        ElderMemberRelation.member_id == current_user.id
    ).all()
    
    elderly_ids = [relation.elder_id for relation in bind_relations]
    
    if not elderly_ids:
        return {"reviews": []}
    
    # 查询这些老人的所有评价
    reviews = db.query(Review).filter(
        Review.elderly_id.in_(elderly_ids)
    ).options(
        joinedload(Review.order).joinedload(Order.items).joinedload(OrderItem.meal)
    ).order_by(
        Review.created_at.desc()
    ).all()
    
    # 格式化返回数据
    result = []
    for review in reviews:
        # 获取餐品名称
        meal_name = ""
        if review.order and review.order.items:
            meal_names = []
            for item in review.order.items:
                if item.meal:
                    meal_names.append(item.meal.name)
            meal_name = "、".join(meal_names)
        
        # 获取餐品图片
        meal_image = None
        if review.order and review.order.items and review.order.items[0].meal:
            meal_image = review.order.items[0].meal.image_url
        
        result.append({
            "id": review.id,
            "order_id": review.order_id,
            "rating": review.rating,
            "content": review.content,
            "images": review.images or [],
            "reply": review.reply,
            "created_at": review.created_at,
            "order": {
                "meal_name": meal_name,
                "meal_image": meal_image
            }
        })
    
    return {"reviews": result}


@router.post("/avatar")
async def upload_member_avatar(
    avatar: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传家属头像"""
    # 验证文件类型
    allowed_extensions = {".jpg", ".jpeg", ".png", ".gif"}
    file_extension = os.path.splitext(avatar.filename)[1].lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="只支持jpg、jpeg、png、gif格式的图片")
    
    # 创建上传目录
    upload_dir = os.path.join("static", "uploads", "avatars")
    os.makedirs(upload_dir, exist_ok=True)
    
    # 生成唯一文件名
    filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(upload_dir, filename)
    
    # 保存文件
    with open(file_path, "wb") as f:
        content = await avatar.read()
        f.write(content)
    
    # 获取用户的家属档案
    from app.models.user import MemberProfile
    member_profile = db.query(MemberProfile).filter(MemberProfile.user_id == current_user.id).first()
    if not member_profile:
        raise HTTPException(status_code=404, detail="用户档案不存在")
    
    # 更新头像URL
    avatar_url = f"http://localhost:7678/static/uploads/avatars/{filename}"
    member_profile.avatar = avatar_url
    db.commit()
    
    return {
        "success": True,
        "message": "头像上传成功",
        "data": {
            "avatar_url": avatar_url
        }
    }