from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Tuple
from pydantic import BaseModel
import re
import uuid
import os
from pathlib import Path

from app.core.database import get_db
from app.core.deps import get_current_user
from app.models.user import User
from app.models.delivery import Delivery
from app.services.order_service import order_service
from app.services.delivery_service import delivery_service

def parse_geography_point(location) -> dict:
    """安全解析PostgreSQL地理空间数据，返回包含latitude和longitude的字典"""
    result = {"latitude": None, "longitude": None}
    
    if not location:
        return result
    
    # PostgreSQL的geography类型可能是二进制格式或文本格式
    try:
        # 尝试直接访问地理空间对象的属性（如果是SQLAlchemy的地理空间类型）
        if hasattr(location, 'x') and hasattr(location, 'y'):
            # SQLAlchemy地理空间对象
            result["longitude"] = float(location.x)
            result["latitude"] = float(location.y)
            return result
    except Exception:
        pass
    
    # 如果不是SQLAlchemy地理空间对象，尝试字符串解析
    location_str = str(location)
    
    # 尝试匹配文本格式：POINT(longitude latitude)
    match = re.match(r'POINT\((-?\d+\.?\d*) (-?\d+\.?\d*)\)', location_str)
    if match:
        try:
            longitude = float(match.group(1))
            latitude = float(match.group(2))
            result["latitude"] = latitude
            result["longitude"] = longitude
        except (ValueError, IndexError):
            pass
    
    # 验证经纬度范围（纬度：-90到90，经度：-180到180）
    if result["latitude"] is not None and result["longitude"] is not None:
        if abs(result["latitude"]) > 90 or abs(result["longitude"]) > 180:
            # 坐标超出合理范围，重置为None
            result["latitude"] = None
            result["longitude"] = None
    
    return result

router = APIRouter(prefix="/deliver", tags=["配送员端"])

class OrderItem(BaseModel):
    id: int
    order_no: str
    elderly_name: str
    delivery_address: str
    delivery_time: str
    distance: str
    total_amount: float
    
    class Config:
        from_attributes = True

class LocationUpdate(BaseModel):
    latitude: str
    longitude: str
    accuracy: float

class CompleteDelivery(BaseModel):
    actual_distance: int
    notes: str

@router.get("/orders", response_model=dict)
def get_orders(
    status: Optional[str] = Query(None, description="订单状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.order import Order
    from app.models.delivery import Delivery
    
    # 根据订单状态采用不同的查询逻辑
    if status == "pending_accept":
        # 待接单订单：所有配送员都可以看到，直接从orders表查询
        query = db.query(Order).filter(Order.status == status)
    else:
        # 其他状态订单：只显示当前配送员的订单，通过deliveries表关联
        query = db.query(Order).join(Delivery, Delivery.order_id == Order.id).filter(Delivery.deliverer_id == current_user.id)
        if status:
            query = query.filter(Order.status == status)
    
    total = query.count()
    skip = (page - 1) * limit
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    orders_data = []
    for order in orders:
        elderly_location = {"latitude": None, "longitude": None}
        
        if order.elderly and order.elderly.elderly_profile and order.elderly.elderly_profile.location:
            # 尝试使用PostgreSQL的ST_AsText函数获取文本格式的地理空间数据
            try:
                # 直接从数据库获取文本格式的地理空间数据
                from sqlalchemy import text
                result = db.execute(text("""
                    SELECT ST_AsText(location) as location_text 
                    FROM elderly_profiles 
                    WHERE user_id = :user_id
                """), {"user_id": order.elderly.id}).fetchone()
                
                if result and result.location_text:
                    location_text = result.location_text
                    # 解析文本格式：POINT(longitude latitude)
                    match = re.match(r'POINT\((-?\d+\.?\d*) (-?\d+\.?\d*)\)', location_text)
                    if match:
                        longitude = float(match.group(1))
                        latitude = float(match.group(2))
                        # 验证经纬度范围
                        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                            elderly_location = {"latitude": latitude, "longitude": longitude}
            except Exception as e:
                print(f"Error parsing location: {e}")
        
        # 构建餐品信息
        meal_items = []
        for item in order.items:
            meal_items.append({
                "name": item.meal.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "subtotal": item.subtotal
            })
        
        # 构建餐品名称字符串，显示所有餐品
        meal_names = [f"{item['name']} x{item['quantity']}" for item in meal_items]
        meal_name_str = "，".join(meal_names) if meal_names else "未知餐品"
        
        orders_data.append({
            "id": order.id,
            "order_number": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:03d}",
            "elderly_name": order.elderly.elderly_profile.name if order.elderly.elderly_profile else order.elderly.username,
            "elderly_phone": order.elderly.elderly_profile.phone if order.elderly.elderly_profile else "",
            "delivery_address": order.delivery_address,
            "community_name": order.elderly.elderly_profile.community.name if order.elderly.elderly_profile and order.elderly.elderly_profile.community else "未知社区",
            "meal_name": meal_name_str,
            "quantity": sum(item.quantity for item in order.items),
            "unit_price": order.items[0].unit_price if order.items else 0,
            "total_amount": order.total_amount,
            "created_at": order.created_at.isoformat(),
            "status": order.status,
            "elderly_location": elderly_location,
            "is_assigned_by_admin": order.delivery.is_assigned_by_admin if order.delivery else False,
            "assigned_deliverer_id": order.delivery.deliverer_id if order.delivery else None,
            "meal_items": meal_items
        })
    
    return {
        "orders": orders_data,
        "total": total,
        "page": page,
        "limit": limit
    }


@router.get("/orders/{order_id}")
def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取订单详情"""
    from app.models.order import Order
    from app.models.delivery import Delivery
    
    # 查询订单
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查权限：待接单订单所有人都能看，其他状态只能看自己的订单
    if order.status != "pending_accept":
        delivery = db.query(Delivery).filter(Delivery.order_id == order_id, Delivery.deliverer_id == current_user.id).first()
        if not delivery:
            raise HTTPException(status_code=403, detail="无权访问此订单")
    
    # 获取配送信息
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    
    # 构建餐品信息
    meal_items = []
    for item in order.items:
        meal_items.append({
            "name": item.meal.name,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "subtotal": item.subtotal
        })
    
    # 构建餐品名称字符串，显示所有餐品
    meal_names = [f"{item['name']} x{item['quantity']}" for item in meal_items]
    meal_name_str = "，".join(meal_names) if meal_names else "未知餐品"
    
    return {
        "success": True,
        "data": {
            "id": order.id,
            "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:03d}",
            "elderly_name": order.elderly.elderly_profile.name if order.elderly.elderly_profile else order.elderly.username,
            "elderly_phone": order.elderly.elderly_profile.phone if order.elderly.elderly_profile else "",
            "delivery_address": order.delivery_address,
            "community_name": order.elderly.elderly_profile.community.name if order.elderly.elderly_profile and order.elderly.elderly_profile.community else "未知社区",
            "meal_name": meal_name_str,
            "quantity": sum(item.quantity for item in order.items),
            "notes": order.notes or "",
            "created_at": order.created_at.strftime("%Y-%m-%d %H:%M"),
            "delivery_time": "12:30前送达",  # 这里可以根据实际业务逻辑计算配送时间
            "distance": f"距离{2.5}km",  # 这里可以根据实际位置计算距离
            "status": order.status,
            "is_assigned_by_admin": delivery.is_assigned_by_admin if delivery else False,
            "assigned_deliverer_id": delivery.deliverer_id if delivery else None,
            "meal_items": meal_items
        }
    }


@router.post("/orders/{order_id}/accept")
def accept_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """接受订单"""
    from app.models.order import Order
    
    # 查询订单
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 检查订单状态
    if order.status != "pending_accept":
        return {
            "success": False,
            "message": "订单状态不允许接单",
            "error_code": "ORDER_STATUS_INVALID"
        }
    
    # 检查订单是否已被指派
    existing_delivery = db.query(Delivery).filter(Delivery.order_id == order_id).first()
    if existing_delivery:
        # 如果是管理员指派的订单，检查当前用户是否是被指派的配送员
        if existing_delivery.is_assigned_by_admin:
            if existing_delivery.deliverer_id != current_user.id:
                return {
                    "success": False,
                    "message": "该订单已被管理员指派，不允许您接单",
                    "error_code": "ORDER_ASSIGNED"
                }
            else:
                # 被指派的配送员可以接单，更新配送状态
                existing_delivery.status = "in_transit"
                order.status = "delivering"
                db.commit()
                return {
                    "success": True,
                    "order_id": order_id,
                    "status": "delivering",
                    "message": "开始配送成功"
                }
        else:
            # 非管理员指派的订单，如果已有配送记录，不允许接单
            return {
                "success": False,
                "message": "该订单已被指派，不允许您接单",
                "error_code": "ORDER_ASSIGNED"
            }
    
    # 普通订单，创建新的配送记录
    try:
        delivery = delivery_service.assign_delivery(db, order_id, current_user.id)
        return {
            "success": True,
            "order_id": order_id,
            "status": "delivering",
            "message": "接单成功"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/orders/{order_id}/complete")
def complete_delivery(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 找到对应的配送记录
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id, Delivery.deliverer_id == current_user.id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="配送记录不存在")
    
    completed_delivery = delivery_service.complete_delivery(db, delivery.id)
    if not completed_delivery:
        raise HTTPException(status_code=400, detail="只能完成配送中的订单")
    
    return {
        "order_id": order_id,
        "status": "completed",
        "message": "配送完成",
        "income": 5.00  # 模拟收入
    }

@router.post("/location")
def update_location(
    location_data: LocationUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    location = delivery_service.update_deliverer_location(
        db,
        current_user.id,
        location_data.latitude,
        location_data.longitude
    )
    if location:
        return {
            "message": "位置更新成功",
            "timestamp": location.get("location_updated_at")
        }
    return {
        "message": "位置更新失败",
        "timestamp": None
    }

@router.get("/orders/delivering")
def get_delivering_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    deliveries = delivery_service.get_deliverer_deliveries(db, current_user.id, status="in_transit")
    
    result = []
    for delivery in deliveries:
        elderly_location = {"latitude": None, "longitude": None}
        
        if delivery.order.elderly and delivery.order.elderly.elderly_profile and delivery.order.elderly.elderly_profile.location:
            # 尝试使用PostgreSQL的ST_AsText函数获取文本格式的地理空间数据
            try:
                # 直接从数据库获取文本格式的地理空间数据
                from sqlalchemy import text
                query_result = db.execute(text("""
                    SELECT ST_AsText(location) as location_text 
                    FROM elderly_profiles 
                    WHERE user_id = :user_id
                """), {"user_id": delivery.order.elderly.id}).fetchone()
                
                if query_result and query_result.location_text:
                    location_text = query_result.location_text
                    # 解析文本格式：POINT(longitude latitude)
                    match = re.match(r'POINT\((-?\d+\.?\d*) (-?\d+\.?\d*)\)', location_text)
                    if match:
                        longitude = float(match.group(1))
                        latitude = float(match.group(2))
                        # 验证经纬度范围
                        if -90 <= latitude <= 90 and -180 <= longitude <= 180:
                            elderly_location = {"latitude": latitude, "longitude": longitude}
            except Exception as e:
                print(f"Error parsing location: {e}")
        
        result.append({
            "id": delivery.order.id,
            "order_no": f"ORD{delivery.order.created_at.strftime('%Y%m%d')}{delivery.order.id:03d}",
            "elderly_name": delivery.order.elderly.elderly_profile.name if delivery.order.elderly.elderly_profile else delivery.order.elderly.username,
            "delivery_address": delivery.order.delivery_address,
            "community_name": delivery.order.elderly.elderly_profile.community.name if delivery.order.elderly.elderly_profile and delivery.order.elderly.elderly_profile.community else "未知社区",
            "delivery_time": delivery.order.created_at.isoformat(),
            "remaining_time": "30分钟",
            "elderly_phone": delivery.order.elderly.elderly_profile.phone if delivery.order.elderly.elderly_profile else "",
            "elderly_location": elderly_location,
            "is_assigned_by_admin": delivery.is_assigned_by_admin
        })
    
    return result

@router.get("/income")
def get_income_statistics(
    time_range: Optional[str] = Query("today", description="时间范围: today, week, month, custom"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取收入统计数据"""
    from app.models.delivery import Delivery, DeliveryStatus
    from datetime import datetime, timedelta, timezone
    
    # 获取配送员的已完成配送记录（只有完成配送才能获得收入）
    deliveries = db.query(Delivery).filter(Delivery.deliverer_id == current_user.id, Delivery.status == DeliveryStatus.DELIVERED).all()
    
    # 计算总收入（从订单获取实际价格）
    total_income = sum(delivery.order.total_amount for delivery in deliveries if delivery.order)
    
    # 计算今日收入
    today_start = datetime.now(timezone.utc).astimezone()
    today_start = today_start.replace(hour=0, minute=0, second=0, microsecond=0)
    today_deliveries = [d for d in deliveries if (d.actual_time if d.actual_time else d.created_at) >= today_start]
    today_income = sum(delivery.order.total_amount for delivery in today_deliveries if delivery.order)
    
    # 计算本月收入
    month_start = datetime.now(timezone.utc).astimezone()
    month_start = month_start.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    month_deliveries = [d for d in deliveries if (d.actual_time if d.actual_time else d.created_at) >= month_start]
    month_income = sum(delivery.order.total_amount for delivery in month_deliveries if delivery.order)
    
    # 计算本周收入
    week_start = datetime.now(timezone.utc).astimezone()
    week_start = week_start - timedelta(days=week_start.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
    week_deliveries = [d for d in deliveries if (d.actual_time if d.actual_time else d.created_at) >= week_start]
    week_income = sum(delivery.order.total_amount for delivery in week_deliveries if delivery.order)
    
    # 根据时间范围过滤配送记录
    filtered_deliveries = deliveries
    if time_range == "today":
        filtered_deliveries = today_deliveries
    elif time_range == "week":
        filtered_deliveries = week_deliveries
    elif time_range == "month":
        filtered_deliveries = month_deliveries
    elif time_range == "custom" and start_date and end_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d").astimezone()
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d").astimezone()
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59, microsecond=999999)
            filtered_deliveries = [d for d in deliveries if start_datetime <= (d.actual_time if d.actual_time else d.created_at) <= end_datetime]
        except ValueError:
            pass
    
    # 获取收入明细
    income_details = []
    for delivery in filtered_deliveries:
        if delivery.order:
            # 构建餐品名称字符串，显示所有餐品
            meal_items = []
            for item in delivery.order.items:
                meal_items.append({
                    "name": item.meal.name,
                    "quantity": item.quantity
                })
            meal_names = [f"{item['name']} x{item['quantity']}" for item in meal_items]
            meal_name_str = "，".join(meal_names) if meal_names else "未知餐品"
            
            # 使用actual_time作为完成时间，如果没有则使用created_at
            time_field = delivery.actual_time if delivery.actual_time else delivery.created_at
            income_details.append({
                "id": delivery.id,
                "order_no": f"ORD{time_field.strftime('%Y%m%d')}{delivery.order.id:03d}",
                "meal_name": meal_name_str,
                "amount": delivery.order.total_amount,  # 使用订单实际金额
                "time": time_field.strftime("%Y-%m-%d %H:%M")
            })
    
    # 按时间倒序排序
    income_details.sort(key=lambda x: x["time"], reverse=True)
    
    # 根据时间范围返回相应的收入数据
    if time_range == "today":
        display_income = today_income
    elif time_range == "week":
        display_income = week_income
    elif time_range == "month":
        display_income = month_income
    else:
        display_income = sum(delivery.order.total_amount for delivery in filtered_deliveries if delivery.order)
    
    return {
        "today_income": today_income,
        "month_income": month_income,
        "total_income": total_income,
        "balance": total_income,  # 可用余额
        "income_details": income_details,
        "display_income": display_income
    }



@router.post("/exceptions")
def report_exception(
    order_id: int,
    exception_type: str,
    description: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delivery = db.query(Delivery).filter(Delivery.order_id == order_id, Delivery.deliverer_id == current_user.id).first()
    if not delivery:
        raise HTTPException(status_code=404, detail="配送记录不存在")
    
    exception = delivery_service.report_exception(db, delivery.id, exception_type, description)
    return {
        "id": exception.id,
        "order_id": order_id,
        "exception_type": exception.type,
        "description": exception.description,
        "status": "reported",
        "created_at": exception.created_at
    }

@router.get("/exceptions")
def get_exceptions(
    status: Optional[str] = Query(None, description="异常状态"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    from app.models.delivery import Exception
    from app.models.order import Order
    from datetime import datetime
    
    # 查询异常记录
    query = db.query(Exception)
    
    # 添加筛选条件
    if status:
        query = query.filter(Exception.type == status)
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Exception.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
        query = query.filter(Exception.created_at <= end_datetime)
    
    # 获取总数
    total = query.count()
    
    # 分页
    skip = (page - 1) * limit
    exceptions = query.order_by(Exception.created_at.desc()).offset(skip).limit(limit).all()
    
    # 构建响应数据
    items = []
    for exception in exceptions:
        # 获取配送信息
        delivery = db.query(Delivery).filter(Delivery.id == exception.delivery_id).first()
        order_info = None
        if delivery:
            order = db.query(Order).filter(Order.id == delivery.order_id).first()
            if order:
                order_info = {
                    "order_id": order.id,
                    "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:03d}",
                    "elderly_name": order.elderly.elderly_profile.name if order.elderly.elderly_profile else order.elderly.username
                }
        
        items.append({
            "id": exception.id,
            "delivery_id": exception.delivery_id,
            "type": exception.type,
            "description": exception.description,
            "created_at": exception.created_at.isoformat(),
            "order": order_info
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/profile")
def get_deliverer_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取配送员个人信息"""
    from app.models.delivery import Delivery, DeliveryStatus
    from datetime import datetime, timedelta
    
    # 获取配送员基本信息
    from app.models.user import DelivererProfile
    profile = db.query(DelivererProfile).filter(DelivererProfile.user_id == current_user.id).first()
    
    deliverer_info = {
        "id": current_user.id,
        "name": profile.name if profile else current_user.username,
        "phone": profile.phone if profile else current_user.username,  # 假设用户名是手机号
        "status": "online",
        "avatar": profile.avatar if profile else None
    }
    
    # 获取配送员的已完成配送记录（与收入明细保持一致）
    deliveries = db.query(Delivery).filter(Delivery.deliverer_id == current_user.id, Delivery.status == DeliveryStatus.DELIVERED).all()
    
    # 计算今日订单数（使用end_time而不是created_at）
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).astimezone()
    today_orders = len([d for d in deliveries if d.end_time and d.end_time >= today_start])
    
    # 总订单数
    total_orders = len(deliveries)
    
    # 计算真实好评率
    from app.models.review import Review
    
    # 获取该配送员的所有已审核评价
    reviews = db.query(Review).filter(
        Review.deliverer_id == current_user.id,
        Review.status == "approved"
    ).all()
    
    if reviews:
        # 统计好评数量（4-5星为好评）
        positive_reviews = [r for r in reviews if r.rating >= 4]
        rating_rate = f"{round(len(positive_reviews) / len(reviews) * 100)}%"
    else:
        rating_rate = "0%"
    
    # 计算总收入（与收入明细完全一致）
    total_income = sum(delivery.order.total_amount for delivery in deliveries if delivery.order)
    
    return {
        "deliverer": deliverer_info,
        "stats": {
            "today_orders": today_orders,
            "total_orders": total_orders,
            "rating_rate": rating_rate,
            "total_income": total_income
        }
    }


@router.get("/personal-info")
def get_deliverer_personal_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取配送员详细个人信息"""
    from app.models.user import DelivererProfile
    
    # 获取配送员个人资料
    profile = db.query(DelivererProfile).filter(DelivererProfile.user_id == current_user.id).first()
    
    if not profile:
        # 如果没有个人资料，创建一个默认的
        profile = DelivererProfile(
            user_id=current_user.id,
            name=current_user.username,
            phone=current_user.username,
            vehicle_type="电动车"
        )
        db.add(profile)
        db.commit()
        db.refresh(profile)
    
    return {
        "name": profile.name,
        "phone": profile.phone,
        "idCard": "",  # 身份证号暂不存储
        "gender": "male",  # 默认性别
        "age": "",  # 年龄暂不存储
        "vehicle_type": profile.vehicle_type,
        "avatar": profile.avatar
    }


@router.get("/reviews")
def get_deliverer_reviews(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取配送员的评价列表"""
    from app.models.review import Review
    from app.models.order import Order
    
    # 查询该配送员的所有评价（经过审核的评价）
    skip = (page - 1) * limit
    
    reviews = db.query(Review).filter(
        Review.deliverer_id == current_user.id,
        Review.status == "approved"
    ).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
    
    # 获取统计数据
    total_reviews = db.query(Review).filter(
        Review.deliverer_id == current_user.id,
        Review.status == "approved"
    ).count()
    
    # 计算平均评分
    avg_rating_result = db.query(func.avg(Review.rating)).filter(
        Review.deliverer_id == current_user.id,
        Review.status == "approved"
    ).scalar()
    average_rating = round(float(avg_rating_result) if avg_rating_result else 0, 1)
    
    # 统计各星级评价数量
    rating_stats = []
    for rating in range(5, 0, -1):
        count = db.query(Review).filter(
            Review.deliverer_id == current_user.id,
            Review.status == "approved",
            Review.rating == rating
        ).count()
        percentage = round((count / total_reviews * 100) if total_reviews > 0 else 0, 1)
        rating_stats.append({
            "rating": rating,
            "count": count,
            "percentage": percentage
        })
    
    # 构建评价详情
    review_items = []
    for review in reviews:
        reviewer_name = ""
        if review.elderly and review.elderly.elderly_profile:
            reviewer_name = review.elderly.elderly_profile.name
        elif review.elderly:
            reviewer_name = review.elderly.username
        
        review_items.append({
            "id": review.id,
            "order_id": review.order_id,
            "reviewer_name": reviewer_name,
            "rating": review.rating,
            "content": review.content,
            "images": review.images or [],
            "reply": review.reply,
            "created_at": review.created_at.strftime("%Y-%m-%d %H:%M"),
            "reviewer_type": review.reviewer_type
        })
    
    return {
        "total": total_reviews,
        "page": page,
        "limit": limit,
        "average_rating": average_rating,
        "total_reviews": total_reviews,
        "rating_stats": rating_stats,
        "reviews": review_items
    }


@router.post("/avatar")
async def upload_deliverer_avatar(
    avatar: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """上传配送员头像"""
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
    
    # 获取用户的配送员档案
    from app.models.user import DelivererProfile
    deliverer_profile = db.query(DelivererProfile).filter(DelivererProfile.user_id == current_user.id).first()
    if not deliverer_profile:
        raise HTTPException(status_code=404, detail="用户档案不存在")
    
    # 更新头像URL
    avatar_url = f"http://localhost:7678/static/uploads/avatars/{filename}"
    deliverer_profile.avatar = avatar_url
    db.commit()
    
    return {
        "success": True,
        "message": "头像上传成功",
        "data": {
            "avatar_url": avatar_url
        }
    }