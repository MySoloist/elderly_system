from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from pydantic import BaseModel

from app.core.database import get_db
from app.core.deps import get_current_user
from datetime import datetime, timezone
from app.models.user import User, UserType, ElderlyProfile
from app.models.community import Community
from app.models.announcement import Announcement
from app.models.review import Review
from app.services.statistic_service import statistic_service
from app.services.meal_service import meal_service
from app.services.community_service import community_service
from app.services.announcement_service import announcement_service
from app.services.review_service import review_service
from app.services.ai_review_service import ai_review_service
from app.services.ai_reply_service import AIReplyService
from app.services.ai_service import AIService
from app.services.ai_analysis_service import AIAnalysisService
from app.services.backup_service import backup_service
from app.services.staff_schedule_service import staff_schedule_service
from app.services.user_service import user_service

# 导入健康标签路由
from app.api.admin.health_tag import router as health_tag_router

router = APIRouter(prefix="/admin", tags=["管理端"])

class UserInfo(BaseModel):
    id: int
    username: str
    user_type: str
    status: str
    profile: dict
    created_at: str
    
    class Config:
        from_attributes = True

class MealCreate(BaseModel):
    name: str
    price: float
    description: str
    category: str
    image_url: Optional[str] = None
    nutrition: Optional[List[str]] = []

class MealUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    status: Optional[str] = None
    nutrition: Optional[List[str]] = []

@router.get("/dashboard")
def get_dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.order import Order
    from app.models.meal import Meal
    from datetime import datetime, timedelta
    
    # 获取统计数据
    stats = statistic_service.get_dashboard_stats(db)
    
    # 获取今日订单数量
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_orders = db.query(func.count(Order.id)).filter(Order.created_at >= today_start).scalar()
    
    # 获取配送中的订单数量
    delivering_orders = db.query(func.count(Order.id)).filter(Order.status == "delivering").scalar()
    
    # 获取餐品总数
    meal_count = db.query(func.count(Meal.id)).scalar()
    
    # 获取社区数量（假设有communities表）
    try:
        from app.models.community import Community
        community_count = db.query(func.count(Community.id)).scalar()
    except:
        community_count = 12  # 默认值
    
    # 获取最近7天的订单趋势和收益数据
    trend_data = []
    revenue_data = []
    print("开始获取订单趋势和收益数据...")
    
    # 从数据库获取真实订单数据和收益数据
    for i in range(6, -1, -1):
        date = (datetime.utcnow() - timedelta(days=i)).date()
        day_start = datetime.combine(date, datetime.min.time())
        day_end = datetime.combine(date, datetime.max.time())
        
        # 获取订单数量
        day_orders = db.query(func.count(Order.id)).filter(
            Order.created_at >= day_start,
            Order.created_at <= day_end
        ).scalar()
        
        # 获取已完成订单的收益
        day_revenue = db.query(func.sum(Order.total_amount)).filter(
            Order.created_at >= day_start,
            Order.created_at <= day_end,
            Order.status == "completed"
        ).scalar()
        
        orders_count = int(day_orders) if day_orders else 0
        revenue_amount = float(day_revenue) if day_revenue else 0
        
        print(f"日期: {date.strftime('%m-%d')}, 订单数: {orders_count}, 收益: {revenue_amount}")
        
        trend_data.append({
            "date": date.strftime("%m-%d"),
            "orders": orders_count
        })
        revenue_data.append({
            "date": date.strftime("%m-%d"),
            "revenue": revenue_amount
        })
    
    print("订单趋势数据:", trend_data)
    print("收益数据:", revenue_data)
    

    
    # 构建前端需要的响应格式
    return {
        "stats": [
            {
                "title": "今日订单总数",
                "value": today_orders or 0,
                "unit": "单",
                "icon": "ShoppingCart",
                "color": "#6366f1",
                "bg": "rgba(99, 102, 241, 0.1)",
                "trend": 12,
                "trendType": "up"
            },
            {
                "title": "平均配送时长",
                "value": stats.get("avg_delivery_time", 22),
                "unit": "分钟",
                "icon": "Timer",
                "color": "#10b981",
                "bg": "rgba(16, 185, 129, 0.1)",
                "trend": 5,
                "trendType": "down"
            },
            {
                "title": "老人总数",
                "value": stats.get("active_elderly", 128),
                "unit": "位",
                "icon": "UserFilled",
                "color": "#6366f1",
                "bg": "rgba(99, 102, 241, 0.1)",
                "trend": 8,
                "trendType": "up"
            },
            {
                "title": "家属总数",
                "value": stats.get("active_members", 96),
                "unit": "位",
                "icon": "User",
                "color": "#8b5cf6",
                "bg": "rgba(139, 92, 246, 0.1)",
                "trend": 15,
                "trendType": "up"
            },
            {
                "title": "跑腿员数量",
                "value": stats.get("active_deliverers", 24),
                "unit": "人",
                "icon": "Van",
                "color": "#ec4899",
                "bg": "rgba(236, 72, 153, 0.1)",
                "trend": 3,
                "trendType": "up"
            },
            {
                "title": "餐品总数",
                "value": meal_count or 86,
                "unit": "种",
                "icon": "Dish",
                "color": "#f59e0b",
                "bg": "rgba(245, 158, 11, 0.1)",
                "trend": 5,
                "trendType": "up"
            },
            {
                "title": "社区数量",
                "value": community_count,
                "unit": "个",
                "icon": "House",
                "color": "#ef4444",
                "bg": "rgba(239, 68, 68, 0.1)",
                "trend": 2,
                "trendType": "up"
            },
            {
                "title": "好评率",
                "value": stats.get("satisfaction_rate", 99.2),
                "unit": "%",
                "icon": "StarFilled",
                "color": "#10b981",
                "bg": "rgba(16, 185, 129, 0.1)",
                "trend": 0.5,
                "trendType": "up"
            }
        ],
        "deliveringOrders": delivering_orders or 0,
        "trendData": trend_data,
        "revenueData": revenue_data
    }

@router.get("/users", response_model=dict)
def get_users(
    user_type: Optional[str] = Query(None, description="用户类型"),
    status: Optional[str] = Query(None, description="用户状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    query = db.query(User)
    
    # 添加筛选条件
    if user_type:
        query = query.filter(User.user_type == user_type)
    if status:
        query = query.filter(User.status == status)
    
    # 获取总数
    total = query.count()
    
    # 分页
    skip = (page - 1) * limit
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    # 构建响应数据
    items = []
    for user in users:
        profile = {}
        if user.user_type == UserType.elderly and user.elderly_profile:
            profile = {
                "name": user.elderly_profile.name,
                "phone": user.elderly_profile.phone,
                "age": user.elderly_profile.age,
                "gender": user.elderly_profile.gender,
                "address": user.elderly_profile.address
            }
        elif user.user_type == UserType.member and user.member_profile:
            profile = {
                "name": user.member_profile.name,
                "phone": user.member_profile.phone
            }
        elif user.user_type == UserType.deliverer and user.deliverer_profile:
            profile = {
                "name": user.deliverer_profile.name,
                "phone": user.deliverer_profile.phone,
                "vehicle_type": user.deliverer_profile.vehicle_type
            }
        elif user.user_type == UserType.ADMIN and user.admin_profile:
            profile = {
                "name": user.admin_profile.name,
                "phone": user.admin_profile.phone
            }
        
        items.append({
            "id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "status": user.status,
            "profile": profile,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat()
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/users/elderly", response_model=dict)
def get_elderly_users(
    status: Optional[str] = Query(None, description="用户状态"),
    community_id: Optional[int] = Query(None, description="社区ID"),
    health_tag_id: Optional[int] = Query(None, description="健康标签ID"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    query = db.query(User).filter(User.user_type == UserType.elderly)
    
    if status:
        query = query.filter(User.status == status)
    
    if community_id:
        query = query.filter(User.elderly_profile.has(community_id=community_id))
    
    if health_tag_id == 0:
        # 查找健康标签为null的老人（良好）
        query = query.filter(User.elderly_profile.has(ElderlyProfile.health_tag_id.is_(None)))
    elif health_tag_id:
        query = query.filter(User.elderly_profile.has(health_tag_id=health_tag_id))
    
    if search:
        search_filter = (
            User.elderly_profile.has(name__icontains=search) |
            User.elderly_profile.has(phone__icontains=search) |
            User.elderly_profile.has(address__icontains=search)
        )
        query = query.filter(search_filter)
    
    total = query.count()
    skip = (page - 1) * limit
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    items = []
    for user in users:
        profile = {}
        if user.elderly_profile:
            profile = {
                "name": user.elderly_profile.name,
                "phone": user.elderly_profile.phone,
                "age": user.elderly_profile.age,
                "gender": user.elderly_profile.gender,
                "address": user.elderly_profile.address,
                "health_status": user.elderly_profile.health_tag.name if user.elderly_profile.health_tag else None,
                "dietary_preferences": user.elderly_profile.dietary_preferences,
                "community_id": user.elderly_profile.community_id,
                "health_tag_id": user.elderly_profile.health_tag_id
            }
            
            # 添加社区信息
            if user.elderly_profile.community:
                profile["community"] = {
                    "id": user.elderly_profile.community.id,
                    "name": user.elderly_profile.community.name
                }
            
            # 添加健康标签信息
            if user.elderly_profile.health_tag:
                profile["health_tag"] = {
                    "id": user.elderly_profile.health_tag.id,
                    "name": user.elderly_profile.health_tag.name,
                    "color": user.elderly_profile.health_tag.color
                }
        
        items.append({
            "id": user.id,
            "username": user.username,
            "status": user.status,
            "profile": profile,
            "created_at": user.created_at.isoformat()
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/users/members", response_model=dict)
def get_member_users(
    status: Optional[str] = Query(None, description="用户状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    query = db.query(User).filter(User.user_type == UserType.member)
    
    if status:
        query = query.filter(User.status == status)
    
    total = query.count()
    skip = (page - 1) * limit
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    items = []
    for user in users:
        profile = {}
        if user.member_profile:
            profile = {
                "name": user.member_profile.name,
                "phone": user.member_profile.phone
            }
        
        items.append({
            "id": user.id,
            "username": user.username,
            "status": user.status,
            "profile": profile,
            "created_at": user.created_at.isoformat()
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/users/deliverers", response_model=dict)
def get_deliverer_users(
    status: Optional[str] = Query(None, description="用户状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    query = db.query(User).filter(User.user_type == UserType.deliverer)
    
    if status:
        query = query.filter(User.status == status)
    
    total = query.count()
    skip = (page - 1) * limit
    users = query.order_by(User.created_at.desc()).offset(skip).limit(limit).all()
    
    items = []
    for user in users:
        profile = {}
        if user.deliverer_profile:
            # 获取配送员最新位置（从 deliverer_profiles 表）
            current_location = None
            if user.deliverer_profile.latitude and user.deliverer_profile.longitude:
                current_location = {
                    "latitude": user.deliverer_profile.latitude,
                    "longitude": user.deliverer_profile.longitude,
                    "timestamp": user.deliverer_profile.location_updated_at.isoformat() if user.deliverer_profile.location_updated_at else None
                }
            
            profile = {
                "name": user.deliverer_profile.name,
                "phone": user.deliverer_profile.phone,
                "vehicle_type": user.deliverer_profile.vehicle_type,
                "current_location": current_location,
                "status": user.deliverer_profile.status,
                "area": {
                    "id": user.deliverer_profile.area.id,
                    "name": user.deliverer_profile.area.name
                } if user.deliverer_profile.area else None
            }
        
        # 统计今日订单数量
        from datetime import datetime, timezone, timedelta
        # 使用本地时区（+08:00）来匹配数据库中的时间
        today_start = datetime.now(timezone.utc).astimezone(timezone(timedelta(hours=8))).replace(hour=0, minute=0, second=0, microsecond=0)
        
        from app.models.order import Order
        from app.models.delivery import Delivery
        
        today_orders_count = db.query(Delivery).join(Order).filter(
            Delivery.deliverer_id == user.id,
            Delivery.end_time >= today_start,
            Order.status == 'completed'
        ).count()
        
        # 计算配送员平均评分
        average_rating = user_service.get_deliverer_average_rating(db, user.id)
        
        items.append({
            "id": user.id,
            "username": user.username,
            "status": user.status,
            "profile": profile,
            "created_at": user.created_at.isoformat(),
            "today_orders": today_orders_count,
            "rating": average_rating
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.get("/deliverer-locations", response_model=dict)
def get_deliverer_locations(
    deliverer_id: Optional[int] = Query(None, description="配送员ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取配送员实时位置"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.user import DelivererProfile
    
    query = db.query(DelivererProfile).filter(
        DelivererProfile.latitude.isnot(None),
        DelivererProfile.longitude.isnot(None)
    )
    if deliverer_id:
        query = query.filter(DelivererProfile.user_id == deliverer_id)
    
    # 获取配送员位置
    profiles = query.all()
    
    result = []
    for profile in profiles:
        result.append({
            "deliverer_id": profile.user_id,
            "latitude": profile.latitude,
            "longitude": profile.longitude,
            "timestamp": profile.location_updated_at.isoformat() if profile.location_updated_at else None
        })
    
    return {
        "locations": result
    }


@router.get("/elder-member-relations", response_model=dict)
def get_elder_member_relations(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    member_id: Optional[int] = Query(None, description="家属ID"),
    elder_id: Optional[int] = Query(None, description="老人ID"),
    name: Optional[str] = Query(None, description="家属姓名"),
    elderly_name: Optional[str] = Query(None, description="老人姓名"),
    phone: Optional[str] = Query(None, description="联系方式"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取老人家属绑定关系列表"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.elder_member_relation import ElderMemberRelation
    from sqlalchemy import or_, and_
    
    query = db.query(ElderMemberRelation)
    
    # 添加家属ID过滤条件
    if member_id:
        query = query.filter(ElderMemberRelation.member_id == member_id)
    
    # 添加老人ID过滤条件
    if elder_id:
        query = query.filter(ElderMemberRelation.elder_id == elder_id)
    
    # 添加搜索条件
    if name or elderly_name or phone:
        conditions = []
        
        if name:
            # 通过家属ID关联查询家属姓名
            member_users = db.query(User).filter(
                User.user_type == "member",
                User.member_profile.has(name=name)
            ).all()
            if member_users:
                member_ids = [user.id for user in member_users]
                conditions.append(ElderMemberRelation.member_id.in_(member_ids))
        
        if elderly_name:
            # 通过老人ID关联查询老人姓名
            elderly_users = db.query(User).filter(
                User.user_type == "elderly",
                User.elderly_profile.has(name=elderly_name)
            ).all()
            if elderly_users:
                elderly_ids = [user.id for user in elderly_users]
                conditions.append(ElderMemberRelation.elder_id.in_(elderly_ids))
        
        if phone:
            # 通过家属ID关联查询联系方式
            member_users = db.query(User).filter(
                User.user_type == "member",
                User.member_profile.has(phone=phone)
            ).all()
            if member_users:
                member_ids = [user.id for user in member_users]
                conditions.append(ElderMemberRelation.member_id.in_(member_ids))
        
        if conditions:
            query = query.filter(or_(*conditions))
    
    total = query.count()
    skip = (page - 1) * limit
    relations = query.order_by(ElderMemberRelation.created_at.desc()).offset(skip).limit(limit).all()
    
    items = []
    for relation in relations:
        # 获取家属信息
        member = db.query(User).filter(User.id == relation.member_id).first()
        member_name = member.member_profile.name if member and member.member_profile else "未知"
        member_phone = member.member_profile.phone if member and member.member_profile else ""
        
        # 获取老人信息
        elderly = db.query(User).filter(User.id == relation.elder_id).first()
        elderly_name = elderly.elderly_profile.name if elderly and elderly.elderly_profile else "未知"
        
        items.append({
            "id": relation.id,
            "member_id": relation.member_id,
            "member_name": member_name,
            "member_phone": member_phone,
            "elder_id": relation.elder_id,
            "elderly_name": elderly_name,
            "relationship": relation.relationship,
            "is_primary": relation.is_primary,
            "created_at": relation.created_at.isoformat()
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


@router.post("/elder-member-relations", response_model=dict)
def create_elder_member_relation(
    relation_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建老人家属绑定关系"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.elder_member_relation import ElderMemberRelation
    
    # 验证必填字段
    if not relation_data.get("member_id"):
        raise HTTPException(status_code=400, detail="家属ID不能为空")
    if not relation_data.get("elder_id"):
        raise HTTPException(status_code=400, detail="老人ID不能为空")
    if not relation_data.get("relationship"):
        raise HTTPException(status_code=400, detail="关系不能为空")
    
    # 检查是否已存在绑定关系
    existing_relation = db.query(ElderMemberRelation).filter(
        ElderMemberRelation.member_id == relation_data["member_id"],
        ElderMemberRelation.elder_id == relation_data["elder_id"]
    ).first()
    
    if existing_relation:
        raise HTTPException(status_code=400, detail="该家属与老人已存在绑定关系")
    
    # 创建新的绑定关系
    new_relation = ElderMemberRelation(
        member_id=relation_data["member_id"],
        elder_id=relation_data["elder_id"],
        relationship=relation_data["relationship"],
        is_primary=relation_data.get("is_primary", False)
    )
    
    db.add(new_relation)
    db.commit()
    db.refresh(new_relation)
    
    # 获取家属信息
    member = db.query(User).filter(User.id == new_relation.member_id).first()
    member_name = member.member_profile.name if member and member.member_profile else "未知"
    
    # 获取老人信息
    elderly = db.query(User).filter(User.id == new_relation.elder_id).first()
    elderly_name = elderly.elderly_profile.name if elderly and elderly.elderly_profile else "未知"
    
    return {
        "id": new_relation.id,
        "member_id": new_relation.member_id,
        "member_name": member_name,
        "elder_id": new_relation.elder_id,
        "elderly_name": elderly_name,
        "relationship": new_relation.relationship,
        "is_primary": new_relation.is_primary,
        "created_at": new_relation.created_at.isoformat(),
        "message": "绑定关系创建成功"
    }

@router.get("/orders", response_model=dict)
def get_orders(
    status: Optional[str] = Query(None, description="订单状态"),
    order_type: Optional[str] = Query(None, description="订单类型"),
    elderly_id: Optional[int] = Query(None, description="老人ID"),
    deliverer_id: Optional[int] = Query(None, description="配送员ID"),
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.order import Order
    from app.models.delivery import Delivery
    from app.models.user import ElderlyProfile, DelivererProfile, User
    from sqlalchemy import and_, or_, func
    from datetime import datetime
    
    query = db.query(Order)
    
    # 添加筛选条件
    if status:
        query = query.filter(Order.status == status)
    if order_type:
        query = query.filter(Order.order_type == order_type)
    if elderly_id:
        query = query.filter(Order.elderly_id == elderly_id)
    if deliverer_id:
        query = query.join(Delivery).filter(Delivery.deliverer_id == deliverer_id)
    if start_date:
        start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
        query = query.filter(Order.created_at >= start_datetime)
    if end_date:
        end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
        end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
        query = query.filter(Order.created_at <= end_datetime)
    
    # 获取总数
    total = query.count()
    
    # 分页
    skip = (page - 1) * limit
    orders = query.order_by(Order.created_at.desc()).offset(skip).limit(limit).all()
    
    # 构建响应数据
    items = []
    for order in orders:
        # 获取老人信息
        elderly = db.query(User).filter(User.id == order.elderly_id).first()
        elderly_name = elderly.elderly_profile.name if elderly and elderly.elderly_profile else "未知"
        
        # 获取配送员信息
        delivery = db.query(Delivery).filter(Delivery.order_id == order.id).first()
        deliverer_name = ""
        if delivery and delivery.deliverer_id:
            deliverer = db.query(User).filter(User.id == delivery.deliverer_id).first()
            deliverer_name = deliverer.deliverer_profile.name if deliverer and deliverer.deliverer_profile else "未知"
        
        # 获取交易ID（从支付记录中获取）
        transaction_id = ""
        if hasattr(order, 'payment') and order.payment:
            transaction_id = order.payment.transaction_id
        
        # 获取订单项信息
        order_items = []
        if hasattr(order, 'items'):
            from app.models.order import OrderItem
            for item in order.items:
                meal_name = item.meal.name if item.meal else "未知餐品"
                order_items.append({
                    "meal_name": meal_name,
                    "quantity": item.quantity,
                    "price": float(item.unit_price)
                })
        
        items.append({
            "id": order.id,
            "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:04d}",
            "transaction_id": transaction_id,
            "elderly_name": elderly_name,
            "deliverer_name": deliverer_name,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "delivery_address": order.delivery_address,
            "notes": order.notes,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
            "scheduled_time": order.scheduled_time.isoformat() if order.scheduled_time else None,
            "order_type": order.order_type,
            "items": order_items
        })
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "items": items
    }


class OrderStatusUpdate(BaseModel):
    status: str


class QuickOrderItem(BaseModel):
    meal_id: int
    quantity: int


class QuickOrderRequest(BaseModel):
    elderly_id: int
    items: List[dict]
    delivery_address: str
    notes: Optional[str] = None
    payment_method: str = "cash"

class AdminProfileUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None

class PasswordChange(BaseModel):
    current_password: str
    new_password: str

class SecuritySettings(BaseModel):
    two_factor_auth: bool
    login_notification: bool
    remote_login_alert: bool


class AssignDeliveryRequest(BaseModel):
    order_id: int
    deliverer_id: int
    estimated_time: Optional[str] = None
    remark: Optional[str] = None


@router.get("/test")
def test_route():
    print("测试路由被调用")
    return {"message": "测试成功"}


@router.get("/test-auth")
def test_auth_route(current_user: User = Depends(get_current_user)):
    print(f"测试认证路由被调用，用户: {current_user}")
    return {"message": "认证测试成功", "user": current_user.username}


@router.get("/orders/{order_id}", response_model=dict)
def get_order_detail(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        print(f"收到订单详情请求，订单ID: {order_id}")
        print(f"当前用户: {current_user}")
        
        if current_user.user_type != UserType.admin:
            raise HTTPException(status_code=403, detail="权限不足")
        
        from app.models.order import Order
        
        # 获取订单信息
        order = db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="订单不存在")
        
        # 返回完整订单信息，包括用户、订单项、支付和配送信息
        return {
            "id": order.id,
            "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:04d}",
            "total_amount": float(order.total_amount),
            "status": order.status,
            "delivery_address": order.delivery_address,
            "notes": order.notes,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat(),
            "elderly": {
                "id": order.elderly.id,
                "name": order.elderly.elderly_profile.name if order.elderly.elderly_profile else "未知",
                "phone": order.elderly.elderly_profile.phone if order.elderly.elderly_profile else "",
                "address": order.elderly.elderly_profile.address if order.elderly.elderly_profile else ""
            } if order.elderly else None,
            "items": [
                {
                    "id": item.id,
                    "meal_id": item.meal_id,
                    "meal_name": item.meal.name if item.meal else "未知餐品",
                    "quantity": item.quantity,
                    "unit_price": float(item.unit_price),
                    "subtotal": float(item.subtotal)
                }
                for item in order.items
            ] if hasattr(order, 'items') and order.items else [],
            "payment": {
                "id": order.payment.id,
                "payment_method": order.payment.payment_method,
                "amount": float(order.payment.amount),
                "status": order.payment.status,
                "transaction_id": order.payment.transaction_id
            } if hasattr(order, 'payment') and order.payment else None,
            "delivery": {
                "id": order.delivery.id,
                "deliverer_id": order.delivery.deliverer_id,
                "deliverer_name": order.delivery.deliverer.deliverer_profile.name if order.delivery.deliverer and order.delivery.deliverer.deliverer_profile else None,
                "status": order.delivery.status,
                "estimated_time": order.delivery.estimated_time.isoformat() if order.delivery.estimated_time else None,
                "actual_time": order.delivery.actual_time.isoformat() if order.delivery.actual_time else None
            } if hasattr(order, 'delivery') and order.delivery else None
        }
    except Exception as e:
        import traceback
        print(f"订单详情API错误: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {str(e)}")


@router.put("/orders/{order_id}/status")
def update_order_status(
    order_id: int,
    status_data: OrderStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.order import Order
    
    # 验证状态值
    valid_statuses = ["pending_payment", "pending_accept", "delivering", "completed", "cancelled"]
    if status_data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的订单状态，有效值为: {', '.join(valid_statuses)}")
    
    # 更新订单状态
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    
    return {
        "id": order.id,
        "status": order.status,
        "message": "订单状态更新成功"
    }


@router.post("/orders/quick")
def quick_order(
    order_data: QuickOrderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    print(f"接收到快速下单请求: {order_data}")
    print(f"老人ID: {order_data.elderly_id}")
    print(f"配送地址: '{order_data.delivery_address}'")
    print(f"地址是否为空: {order_data.delivery_address == ''}")
    
    from app.models.order import Order, OrderItem
    from app.models.meal import Meal
    from app.models.delivery import Delivery
    from app.services.order_service import order_service
    
    # 验证老人是否存在
    elderly = db.query(User).filter(User.id == order_data.elderly_id, User.user_type == UserType.elderly).first()
    if not elderly:
        raise HTTPException(status_code=404, detail="老人用户不存在")
    
    print(f"找到老人: {elderly.username}, 姓名: {elderly.elderly_profile.name if elderly.elderly_profile else '无'}")
    
    # 创建订单
    try:
        # 检查items的数据类型
        print(f"items数据类型: {type(order_data.items)}")
        print(f"items内容: {order_data.items}")
        
        # 如果items是字典列表，直接使用
        if order_data.items and isinstance(order_data.items[0], dict):
            order_items = order_data.items
        else:
            # 如果是对象列表，转换为字典
            order_items = [{"meal_id": item.meal_id, "quantity": item.quantity} for item in order_data.items]
        
        print(f"订单项: {order_items}")
        
        print("开始创建订单...")
        order = order_service.create_order(
            db=db,
            user_id=order_data.elderly_id,
            items=order_items,
            delivery_address=order_data.delivery_address,
            notes=order_data.notes
        )
        print(f"订单创建成功: {order.id}")
        
        # 更新支付信息
        order.payment_method = order_data.payment_method
        order.payment_status = "paid" if order_data.payment_method == "cash" else "pending"
        order.status = "pending_accept"
        
        db.commit()
        db.refresh(order)
        
        # 获取老人信息
        elderly_name = elderly.elderly_profile.name if elderly.elderly_profile else "未知"
        
        return {
            "id": order.id,
            "order_no": f"ORD{order.created_at.strftime('%Y%m%d')}{order.id:04d}",
            "elderly_name": elderly_name,
            "total_amount": float(order.total_amount),
            "status": order.status,
            "message": "快速下单成功"
        }
        
    except ValueError as e:
        db.rollback()
        print(f"订单创建失败 (ValueError): {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        db.rollback()
        print(f"订单创建失败 (Exception): {str(e)}")
        import traceback
        print("详细错误信息:")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"创建订单失败: {str(e)}")


@router.post("/deliveries/assign")
def assign_delivery(
    assign_data: AssignDeliveryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.order import Order
    from app.models.delivery import Delivery, DeliveryStatus
    from datetime import datetime
    
    # 验证订单是否存在
    order = db.query(Order).filter(Order.id == assign_data.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 验证订单状态是否可以指派配送
    if order.status not in ["pending_accept", "pending_payment"]:
        raise HTTPException(status_code=400, detail=f"订单状态 {order.status} 不允许指派配送")
    
    # 验证配送员是否存在
    deliverer = db.query(User).filter(User.id == assign_data.deliverer_id, User.user_type == UserType.deliverer).first()
    if not deliverer:
        raise HTTPException(status_code=404, detail="配送员不存在")
    
    # 检查是否已有配送记录
    existing_delivery = db.query(Delivery).filter(Delivery.order_id == assign_data.order_id).first()
    if existing_delivery:
        # 更新现有配送记录
        existing_delivery.deliverer_id = assign_data.deliverer_id
        existing_delivery.status = DeliveryStatus.ASSIGNED
        existing_delivery.is_assigned_by_admin = True
        if assign_data.estimated_time:
            # 将时间字符串转换为完整的datetime对象（当天的指定时间）
            time_obj = datetime.strptime(assign_data.estimated_time, "%H:%M").time()
            existing_delivery.estimated_time = datetime.combine(datetime.now().date(), time_obj)
        delivery = existing_delivery
    else:
        # 创建新的配送记录
        delivery_data = {
            "order_id": assign_data.order_id,
            "deliverer_id": assign_data.deliverer_id,
            "status": DeliveryStatus.ASSIGNED,
            "is_assigned_by_admin": True
        }
        if assign_data.estimated_time:
            # 将时间字符串转换为完整的datetime对象（当天的指定时间）
            time_obj = datetime.strptime(assign_data.estimated_time, "%H:%M").time()
            delivery_data["estimated_time"] = datetime.combine(datetime.now().date(), time_obj)
        
        delivery = Delivery(**delivery_data)
        db.add(delivery)
    
    # 更新订单状态
    order.status = "pending_accept"
    
    db.commit()
    db.refresh(delivery)
    
    # 获取配送员信息
    deliverer_name = deliverer.deliverer_profile.name if deliverer.deliverer_profile else "未知"
    
    return {
        "id": delivery.id,
        "order_id": delivery.order_id,
        "deliverer_id": delivery.deliverer_id,
        "deliverer_name": deliverer_name,
        "status": delivery.status,
        "estimated_time": delivery.estimated_time.isoformat() if delivery.estimated_time else None,
        "message": "配送指派成功"
    }

@router.get("/categories", response_model=dict)
def get_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取所有分类列表"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.models.meal import Category
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


@router.get("/meals", response_model=dict)
def get_meals(
    category: Optional[str] = Query(None, description="分类"),
    tag: Optional[str] = Query(None, description="标签"),
    status: Optional[str] = Query(None, description="状态"),
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    skip = (page - 1) * limit
    meals = meal_service.get_meals(db, category=category, tag=tag, skip=skip, limit=limit)
    
    return {
        "total": len(meals),
        "page": page,
        "limit": limit,
        "items": [
            {
                "id": meal.id,
                "name": meal.name,
                "price": meal.price,
                "description": meal.description,
                "category": meal.category.name if meal.category else None,
                "status": meal.status,
                "image_url": meal.image_url,
                "created_at": meal.created_at
            }
            for meal in meals
        ]
    }

@router.post("/meals")
def create_meal(
    meal_data: MealCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    meal = meal_service.create_meal(
        db,
        name=meal_data.name,
        description=meal_data.description,
        price=meal_data.price,
        category=meal_data.category,
        image_url=meal_data.image_url,
        nutrition=meal_data.nutrition
    )
    return {
        "id": meal.id,
        "name": meal.name,
        "price": meal.price,
        "status": meal.status
    }

@router.put("/meals/{meal_id}")
def update_meal(
    meal_id: int,
    meal_data: MealUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    update_data = meal_data.dict(exclude_unset=True)
    meal = meal_service.update_meal(db, meal_id, **update_data)
    if not meal:
        raise HTTPException(status_code=404, detail="餐品不存在")
    
    return {
        "id": meal.id,
        "name": meal.name,
        "price": meal.price,
        "status": meal.status
    }

@router.delete("/meals/{meal_id}")
def delete_meal(
    meal_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = meal_service.delete_meal(db, meal_id)
    if not success:
        raise HTTPException(status_code=404, detail="餐品不存在")
    
    return {"message": "餐品删除成功", "meal_id": meal_id}

@router.get("/statistics")
def get_statistics(
    start_date: Optional[str] = Query(None, description="开始日期"),
    end_date: Optional[str] = Query(None, description="结束日期"),
    group_by: Optional[str] = Query(None, description="分组方式"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    order_stats = statistic_service.get_order_statistics(db)
    user_stats = statistic_service.get_user_statistics(db)
    delivery_stats = statistic_service.get_delivery_statistics(db)
    
    return {
        "order_statistics": order_stats,
        "delivery_statistics": delivery_stats,
        "user_statistics": user_stats,
        "trends": [
            {
                "date": "2024-01-15",
                "orders": 156,
                "amount": 4446.00
            }
        ]
    }


# 社区管理相关接口
@router.get("/communities", response_model=dict)
def get_communities(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    skip = (page - 1) * limit
    communities = community_service.get_communities(db, skip=skip, limit=limit)
    
    return {
        "total": db.query(Community).count(),
        "page": page,
        "limit": limit,
        "items": [
            {
                "id": community.id,
                "name": community.name,
                "address": community.address,
                "contact_phone": community.contact_phone,
                "manager_name": community.manager_name,
                "manager_phone": community.manager_phone,
                "elderly_count": db.query(User).join(ElderlyProfile).filter(ElderlyProfile.community_id == community.id).count(),
                "status": community.status,
                "created_at": community.created_at
            }
            for community in communities
        ]
    }


@router.get("/communities/{community_id}", response_model=dict)
def get_community(
    community_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    community = community_service.get_community(db, community_id)
    if not community:
        raise HTTPException(status_code=404, detail="社区不存在")
    
    return {
        "id": community.id,
        "name": community.name,
        "address": community.address,
        "contact_phone": community.contact_phone,
        "manager_name": community.manager_name,
        "manager_phone": community.manager_phone,
        "elderly_count": db.query(User).join(ElderlyProfile).filter(ElderlyProfile.community_id == community.id).count(),
        "status": community.status,
        "created_at": community.created_at
    }


@router.post("/communities", response_model=dict)
def create_community(
    community_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    community = community_service.create_community(
        db,
        name=community_data.get("name"),
        address=community_data.get("address"),
        contact_phone=community_data.get("contact_phone"),
        manager_name=community_data.get("manager_name"),
        manager_phone=community_data.get("manager_phone"),
        status=community_data.get("status", "正常")
    )
    
    return {
        "message": "社区创建成功",
        "community": {
            "id": community.id,
            "name": community.name,
            "address": community.address,
            "contact_phone": community.contact_phone,
            "manager_name": community.manager_name,
            "manager_phone": community.manager_phone,
            "elderly_count": 0,  # 新创建的社区没有老人
            "status": community.status
        }
    }


@router.put("/communities/{community_id}", response_model=dict)
def update_community(
    community_id: int,
    community_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    community = community_service.update_community(db, community_id, **community_data)
    if not community:
        raise HTTPException(status_code=404, detail="社区不存在")
    
    return {
        "message": "社区更新成功",
        "community": {
            "id": community.id,
            "name": community.name,
            "address": community.address,
            "contact_phone": community.contact_phone,
            "manager_name": community.manager_name,
            "manager_phone": community.manager_phone,
            "elderly_count": db.query(User).join(ElderlyProfile).filter(ElderlyProfile.community_id == community.id).count(),
            "status": community.status
        }
    }


@router.delete("/communities/{community_id}", response_model=dict)
def delete_community(
    community_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = community_service.delete_community(db, community_id)
    if not success:
        raise HTTPException(status_code=404, detail="社区不存在")
    
    return {"message": "社区删除成功", "community_id": community_id}


# 通知管理相关接口
@router.get("/announcements", response_model=dict)
def get_announcements(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    skip = (page - 1) * limit
    announcements = announcement_service.get_announcements(db, skip=skip, limit=limit)
    
    return {
        "total": db.query(Announcement).count(),
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
                "created_at": announcement.created_at
            }
            for announcement in announcements
        ]
    }


@router.get("/announcements/{announcement_id}", response_model=dict)
def get_announcement(
    announcement_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    announcement = announcement_service.get_announcement(db, announcement_id)
    if not announcement:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {
        "id": announcement.id,
        "title": announcement.title,
        "content": announcement.content,
        "type": announcement.type,
        "priority": announcement.priority,
        "status": announcement.status,
        "created_at": announcement.created_at
    }


@router.post("/announcements", response_model=dict)
def create_announcement(
    announcement_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    announcement = announcement_service.create_announcement(
        db,
        title=announcement_data.get("title"),
        content=announcement_data.get("content"),
        announcement_type=announcement_data.get("type"),
        priority=announcement_data.get("priority", "normal"),
        status=announcement_data.get("status", "active")
    )
    
    return {
        "message": "通知创建成功",
        "announcement": {
            "id": announcement.id,
            "title": announcement.title,
            "content": announcement.content,
            "type": announcement.type,
            "priority": announcement.priority,
            "status": announcement.status
        }
    }


@router.put("/announcements/{announcement_id}", response_model=dict)
def update_announcement(
    announcement_id: int,
    announcement_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    announcement = announcement_service.update_announcement(db, announcement_id, **announcement_data)
    if not announcement:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {
        "message": "通知更新成功",
        "announcement": {
            "id": announcement.id,
            "title": announcement.title,
            "content": announcement.content,
            "type": announcement.type,
            "priority": announcement.priority,
            "status": announcement.status
        }
    }


@router.delete("/announcements/{announcement_id}", response_model=dict)
def delete_announcement(
    announcement_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = announcement_service.delete_announcement(db, announcement_id)
    if not success:
        raise HTTPException(status_code=404, detail="通知不存在")
    
    return {"message": "通知删除成功", "announcement_id": announcement_id}


# 评价管理相关接口
@router.get("/reviews", response_model=dict)
def get_reviews(
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    skip = (page - 1) * limit
    reviews = review_service.get_reviews(db, skip=skip, limit=limit)
    
    # 调试：检查返回的数据
    print(f"返回的评价数量: {len(reviews)}")
    for review in reviews:
        print(f"评价ID: {review.id}, status: {review.status}")
    
    # 获取统计数据
    total_reviews = db.query(Review).count()
    total_positive = db.query(Review).filter(Review.rating >= 4).count()
    total_neutral = db.query(Review).filter(Review.rating == 3).count()
    total_negative = db.query(Review).filter(Review.rating <= 2).count()
    total_with_images = db.query(Review).filter(Review.images.isnot(None), Review.images != []).count()
    total_pending_review = db.query(Review).filter(Review.status == 'pending').count()
    total_approved = db.query(Review).filter(Review.status == 'approved').count()
    total_rejected = db.query(Review).filter(Review.status == 'rejected').count()
    total_pending_reply = db.query(Review).filter((Review.reply.is_(None)) | (Review.reply == "")).count()
    
    # 统计配送评价和餐品评价数量
    total_deliverer_reviews = db.query(Review).filter(Review.deliverer_id.isnot(None)).count()
    total_meal_reviews = db.query(Review).filter(Review.deliverer_id.is_(None)).count()
    
    # 统计配送评价的好评、中评、差评数量
    total_deliverer_positive = db.query(Review).filter(Review.deliverer_id.isnot(None), Review.rating >= 4).count()
    total_deliverer_neutral = db.query(Review).filter(Review.deliverer_id.isnot(None), Review.rating == 3).count()
    total_deliverer_negative = db.query(Review).filter(Review.deliverer_id.isnot(None), Review.rating <= 2).count()
    
    # 统计餐品评价的好评、中评、差评数量
    total_meal_positive = db.query(Review).filter(Review.deliverer_id.is_(None), Review.rating >= 4).count()
    total_meal_neutral = db.query(Review).filter(Review.deliverer_id.is_(None), Review.rating == 3).count()
    total_meal_negative = db.query(Review).filter(Review.deliverer_id.is_(None), Review.rating <= 2).count()
    
    return {
        "total": total_reviews,
        "page": page,
        "limit": limit,
        "stats": {
            "total": total_reviews,
            "positive": total_positive,
            "neutral": total_neutral,
            "negative": total_negative,
            "with_images": total_with_images,
            "pending_review": total_pending_review,
            "approved": total_approved,
            "rejected": total_rejected,
            "pending_reply": total_pending_reply,
            "deliverer_reviews": total_deliverer_reviews,
            "meal_reviews": total_meal_reviews,
            "deliverer_positive": total_deliverer_positive,
            "deliverer_neutral": total_deliverer_neutral,
            "deliverer_negative": total_deliverer_negative,
            "meal_positive": total_meal_positive,
            "meal_neutral": total_meal_neutral,
            "meal_negative": total_meal_negative
        },
        "items": [
            {
                "id": review.id,
                "order_id": review.order_id,
                "elderly_id": review.elderly_id,
                "elderly_name": review.elderly.username if review.elderly else None,
                "rating": review.rating,
                "content": review.content,
                "status": review.status,
                "images": review.images or [],
                "reply": review.reply,
                "created_at": review.created_at,
                "ai_reviewed": review.ai_reviewed,
                "ai_replied": review.ai_replied,
                "mealName": review.order.items[0].meal.name if review.order and review.order.items else "未知餐品",
                "reviewer_type": review.reviewer_type,
                "deliverer_id": review.deliverer_id,
                "deliverer_name": review.deliverer.deliverer_profile.name if review.deliverer and review.deliverer.deliverer_profile else None,
                "deliverer_phone": review.deliverer.deliverer_profile.phone if review.deliverer and review.deliverer.deliverer_profile else None
            }
            for review in reviews
        ]
    }


# AI分析相关接口
@router.get("/reviews/analysis")
async def analyze_reviews(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """AI智能分析评价数据"""
    try:
        if current_user.user_type != UserType.admin:
            raise HTTPException(status_code=403, detail="权限不足")
        
        # 获取所有已审核的评价
        reviews = db.query(Review).filter(Review.status == 'approved').all()
        
        # 转换为字典格式
        reviews_data = []
        for review in reviews:
            reviews_data.append({
                "id": review.id,
                "content": review.content,
                "rating": review.rating,
                "created_at": review.created_at.isoformat() if review.created_at else None,
                "elderly_id": review.elderly_id,
                "deliverer_id": review.deliverer_id,
                "reviewer_type": review.reviewer_type
            })
        
        # 使用AI分析服务进行分析（异步调用）
        ai_service = AIAnalysisService()
        analysis_result = await ai_service.analyze_reviews(reviews_data)
        
        return {
            "success": True,
            "data": analysis_result
        }
    except Exception as e:
        # 记录错误信息
        import traceback
        print(f"AI分析错误: {str(e)}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"AI分析失败: {str(e)}")


@router.get("/reviews/{review_id}", response_model=dict)
def get_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    return {
        "id": review.id,
        "order_id": review.order_id,
        "elderly_id": review.elderly_id,
        "elderly_name": review.elderly.username if review.elderly else None,
        "rating": review.rating,
        "content": review.content,
        "created_at": review.created_at
    }

# 注册健康标签路由
router.include_router(health_tag_router)


@router.post("/reviews", response_model=dict)
def create_review(
    review_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.create_review(
        db,
        order_id=review_data.get("order_id"),
        elderly_id=review_data.get("elderly_id"),
        rating=review_data.get("rating"),
        content=review_data.get("content"),
        reviewer_type="elderly"
    )
    
    return {
        "message": "评价创建成功",
        "review": {
            "id": review.id,
            "order_id": review.order_id,
            "elderly_id": review.elderly_id,
            "rating": review.rating,
            "content": review.content
        }
    }


@router.put("/reviews/{review_id}", response_model=dict)
def update_review(
    review_id: int,
    review_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.update_review(db, review_id, **review_data)
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    return {
        "message": "评价更新成功",
        "review": {
            "id": review.id,
            "order_id": review.order_id,
            "elderly_id": review.elderly_id,
            "rating": review.rating,
            "content": review.content
        }
    }


@router.delete("/reviews/{review_id}", response_model=dict)
def delete_review(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = review_service.delete_review(db, review_id)
    if not success:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    return {"message": "评价删除成功", "review_id": review_id}





# 用户管理相关接口
@router.post("/users", response_model=dict)
def create_user(
    user_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建用户"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 创建用户
    user = user_service.create_user(
        db=db,
        username=user_data.get("username"),
        password=user_data.get("password"),
        user_type=user_data.get("user_type")
    )
    
    # 更新用户资料
    if user_data.get("profile"):
        user_service.update_user_profile(db, user, user_data.get("profile"))
    
    return {
        "message": "用户创建成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "status": user.status
        }
    }


@router.put("/users/{user_id}", response_model=dict)
def update_user(
    user_id: int,
    user_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户信息"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 获取用户
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户基本信息
    if "username" in user_data:
        user.username = user_data["username"]
    if "status" in user_data:
        user.status = user_data["status"]
    
    # 更新用户资料
    if user_data.get("profile"):
        user_service.update_user_profile(db, user, user_data.get("profile"))
    
    db.commit()
    db.refresh(user)
    
    return {
        "message": "用户更新成功",
        "user": {
            "id": user.id,
            "username": user.username,
            "user_type": user.user_type,
            "status": user.status
        }
    }


@router.delete("/users/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除用户"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 获取用户
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 删除用户
    db.delete(user)
    db.commit()
    
    return {"message": "用户删除成功", "user_id": user_id}


@router.post("/reviews/ai-review/batch")
def batch_ai_review(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量AI审核评价"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 获取待审核的评价
    pending_reviews = db.query(Review).filter(Review.status == 'pending').all()
    
    if not pending_reviews:
        return {"message": "没有待审核的评价"}
    
    # AI批量分析
    ai_results = ai_review_service.batch_analyze_reviews(pending_reviews)
    
    # 应用自动审核结果
    auto_approved_count = 0
    auto_rejected_count = 0
    pending_count = 0
    auto_replied_count = 0
    
    for result in ai_results:
        review = next((r for r in pending_reviews if r.id == result['review_id']), None)
        if review:
            update_data = {}
            
            if ai_review_service.should_auto_approve(result):
                update_data['status'] = 'approved'
                auto_approved_count += 1
            elif ai_review_service.should_auto_reject(result):
                update_data['status'] = 'rejected'
                auto_rejected_count += 1
            else:
                pending_count += 1
                continue
            
            # 应用自动回复（如果有）
            if result.get('auto_reply') and not review.reply:
                update_data['reply'] = result['auto_reply']
                auto_replied_count += 1
            
            # 更新评价
            if update_data:
                update_data['ai_reviewed'] = 1  # 标记为AI审核
                review_service.update_review(db, review.id, **update_data)
    
    return {
        "message": "AI审核完成",
        "total_reviews": len(pending_reviews),
        "auto_approved": auto_approved_count,
        "auto_rejected": auto_rejected_count,
        "pending_review": pending_count,
        "auto_replied": auto_replied_count,
        "ai_results": ai_results
    }


@router.post("/reviews/{review_id}/ai-review")
def ai_review_single(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """单个评价AI审核"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    # AI分析
    ai_result = ai_review_service.analyze_review(review)
    
    return {
        "review_id": review_id,
        "ai_analysis": ai_result
    }


@router.post("/reviews/ai-review/apply")
def apply_ai_review(
    review_ids: List[int],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """应用AI审核结果"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    results = []
    for review_id in review_ids:
        review = review_service.get_review(db, review_id)
        if review:
            ai_result = ai_review_service.analyze_review(review)
            
            if ai_review_service.should_auto_approve(ai_result):
                review_service.update_review(db, review_id, status='approved')
                results.append({
                    "review_id": review_id,
                    "action": "approved",
                    "reason": ai_result['reason']
                })
            elif ai_review_service.should_auto_reject(ai_result):
                review_service.update_review(db, review_id, status='rejected')
                results.append({
                    "review_id": review_id,
                    "action": "rejected",
                    "reason": ai_result['reason']
                })
            else:
                results.append({
                    "review_id": review_id,
                    "action": "pending",
                    "reason": "需要人工审核"
                })
    
    return {
        "message": "AI审核结果应用完成",
        "results": results
    }


@router.post("/reviews/{review_id}/ai-reply")
def ai_reply_single(
    review_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """单个评价AI回复"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    if review.reply:
        raise HTTPException(status_code=400, detail="该评价已有回复")
    
    # AI生成回复
    ai_result = AIReplyService.generate_reply(review)
    
    return {
        "message": "AI回复生成成功",
        "review_id": review_id,
        "reply": ai_result['reply'],
        "ai_generated": ai_result['ai_generated'],
        "confidence": ai_result['confidence'],
        "error": ai_result['error']
    }


@router.post("/reviews/ai-reply/batch")
def ai_reply_batch(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量AI回复（处理所有已审核但未回复的评价）"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 获取所有已审核但未回复的评价
    unreplied_reviews = db.query(Review).filter(
        Review.status == 'approved',
        (Review.reply.is_(None)) | (Review.reply == "")
    ).all()
    
    if not unreplied_reviews:
        return {
            "message": "没有未回复的评价",
            "total_reviews": 0,
            "generated_replies": 0,
            "results": []
        }
    
    # 批量生成回复
    ai_results = AIReplyService.batch_generate_replies(unreplied_reviews)
    
    # 应用回复
    applied_count = 0
    for result in ai_results['results']:
        review_service.update_review(db, result['review_id'], reply=result['reply'], ai_replied=1)
        applied_count += 1
    
    return {
        "message": "AI批量回复完成",
        "total_reviews": ai_results['total_reviews'],
        "generated_replies": ai_results['generated_replies'],
        "applied_replies": applied_count,
        "results": ai_results['results']
    }


@router.post("/reviews/{review_id}/apply-reply")
def apply_ai_reply(
    review_id: int,
    reply_content: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """应用AI回复到评价"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review = review_service.get_review(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="评价不存在")
    
    # 更新回复
    review_service.update_review(db, review_id, reply=reply_content, ai_replied=1)
    
    return {
        "message": "回复应用成功",
        "review_id": review_id,
        "reply": reply_content
    }


@router.post("/reviews/batch-approve")
def batch_approve_reviews(
    request_data: dict,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量通过评价"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    review_ids = request_data.get("review_ids", [])
    
    if not review_ids:
        raise HTTPException(status_code=400, detail="评价ID列表不能为空")
    
    # 批量更新评价状态为approved
    for review_id in review_ids:
        review = review_service.get_review(db, review_id)
        if review:
            review_service.update_review(db, review_id, status="approved")
    
    return {
        "message": "批量审核通过成功",
        "review_ids": review_ids,
        "processed_count": len(review_ids)
    }


# AI对话相关的数据模型
class AIQuery(BaseModel):
    query: str


class AIResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: str


# AI对话服务实例
ai_service = AIService()


@router.post("/ai/query", response_model=AIResponse)
async def admin_ai_query(
    ai_query: AIQuery,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """管理员AI对话查询"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 生成AI回复（管理员类型）
    ai_response = await ai_service.generate_ai_response(ai_query.query, user_type="admin")
    
    # 创建对话记录
    conversation = ai_service.create_conversation(
        db=db,
        user_id=current_user.id,
        user_query=ai_query.query,
        ai_response=ai_response,
        conversation_type="admin_assistant"
    )
    
    return AIResponse(
        response=ai_response,
        conversation_id=conversation.conversation_id,
        timestamp=conversation.created_at.isoformat()
    )


@router.get("/ai/conversations")
def get_admin_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取管理员的AI对话记录"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    conversations = ai_service.get_user_conversations(db, current_user.id)
    
    return {
        "total": len(conversations),
        "conversations": [
            {
                "id": conv.id,
                "conversation_id": conv.conversation_id,
                "user_query": conv.user_query,
                "ai_response": conv.ai_response,
                "created_at": conv.created_at.isoformat()
            }
            for conv in conversations
        ]
    }


@router.get("/profile")
def get_admin_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取管理员个人信息"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 调试：打印当前用户信息
    print(f"Current user: {current_user.username}, ID: {current_user.id}, Type: {current_user.user_type}")
    
    # 重新查询用户并加载关联的admin_profile
    admin_user = db.query(User).filter(User.id == current_user.id).first()
    
    # 调试：检查关联关系
    print(f"Admin profile exists: {admin_user.admin_profile is not None}")
    if admin_user.admin_profile:
        print(f"Admin profile name: {admin_user.admin_profile.name}")
        print(f"Admin profile phone: {admin_user.admin_profile.phone}")
    
    return {
        "username": admin_user.username,
        "user_type": admin_user.user_type.value,
        "email": admin_user.email,
        "phone": admin_user.admin_profile.phone if admin_user.admin_profile else None,
        "name": admin_user.admin_profile.name if admin_user.admin_profile else None,
        "created_at": admin_user.created_at.isoformat(),
        "last_login": admin_user.last_login.isoformat() if admin_user.last_login else None
    }


@router.put("/profile")
def update_admin_profile(
    profile_data: AdminProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新管理员个人信息"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    admin = db.query(User).filter(User.id == current_user.id).first()
    
    # 更新用户信息
    if profile_data.username:
        admin.username = profile_data.username
    if profile_data.email:
        admin.email = profile_data.email
    
    # 更新管理员资料
    if admin.admin_profile:
        if profile_data.name:
            admin.admin_profile.name = profile_data.name
        if profile_data.phone:
            admin.admin_profile.phone = profile_data.phone
    
    db.commit()
    db.refresh(admin)
    
    return {
        "username": admin.username,
        "email": admin.email,
        "name": admin.admin_profile.name if admin.admin_profile else None,
        "phone": admin.admin_profile.phone if admin.admin_profile else None
    }


@router.post("/profile/password")
def change_password(
    password_data: PasswordChange,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """修改密码"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from app.core.security import verify_password, get_password_hash
    
    # 验证当前密码
    if not verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="当前密码错误")
    
    # 更新密码
    current_user.password_hash = get_password_hash(password_data.new_password)
    db.commit()
    
    return {"message": "密码修改成功"}


@router.put("/profile/security")
def update_security_settings(
    security_data: SecuritySettings,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新安全设置"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 这里可以保存安全设置到数据库
    # 目前只是返回成功消息
    
    return {
        "message": "安全设置保存成功",
        "settings": security_data.model_dump()
    }


class AISettings(BaseModel):
    chat_model: str
    elderly_chat_model: str
    review_model: str
    api_url: str
    api_key: str


@router.get("/settings/ai")
def get_ai_settings(
    current_user: User = Depends(get_current_user)
):
    """获取AI设置"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    # 从环境变量读取AI配置
    import os
    from app.core.config import settings
    
    return {
        "chat_model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "elderly_chat_model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "review_model": os.getenv("DEEPSEEK_MODEL", "deepseek-chat"),
        "api_url": os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com"),
        "api_key": os.getenv("DEEPSEEK_API_KEY", "")
    }


@router.put("/settings/ai")
def update_ai_settings(
    ai_data: AISettings,
    current_user: User = Depends(get_current_user)
):
    """更新AI设置"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    try:
        import os
        # 更新.env文件中的AI配置
        # 使用绝对路径指向项目根目录的.env文件
        env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), '.env')
        
        print(f"尝试更新.env文件: {env_path}")
        
        # 检查文件是否存在
        if not os.path.exists(env_path):
            raise Exception(f".env文件不存在: {env_path}")
        
        # 读取现有.env文件
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 更新或添加AI配置
        updated = False
        new_lines = []
        
        for line in lines:
            original_line = line
            line = line.strip()
            if line.startswith('DEEPSEEK_API_KEY='):
                new_lines.append(f'DEEPSEEK_API_KEY="{ai_data.api_key}"\n')
                updated = True
            elif line.startswith('DEEPSEEK_API_URL='):
                new_lines.append(f'DEEPSEEK_API_URL="{ai_data.api_url}"\n')
                updated = True
            elif line.startswith('DEEPSEEK_MODEL='):
                new_lines.append(f'DEEPSEEK_MODEL="{ai_data.chat_model}"\n')
                updated = True
            else:
                new_lines.append(original_line)
        
        # 如果没有找到对应的配置，添加它们
        if not updated:
            new_lines.append(f'DEEPSEEK_API_KEY="{ai_data.api_key}"\n')
            new_lines.append(f'DEEPSEEK_API_URL="{ai_data.api_url}"\n')
            new_lines.append(f'DEEPSEEK_MODEL="{ai_data.chat_model}"\n')
        
        # 写回.env文件
        with open(env_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
            
        print(f".env文件更新成功")
        return {
            "message": "AI设置保存成功，已更新.env文件",
            "settings": ai_data.model_dump()
        }
        
    except Exception as e:
        print(f"更新.env文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"保存设置失败: {str(e)}")


@router.get("/settings/ai/models")
def get_ai_models(
    api_url: str,
    api_key: str = None,
    current_user: User = Depends(get_current_user)
):
    """获取可用的AI模型列表"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    import httpx
    
    models = []
    
    try:
        if "deepseek" in api_url.lower():
            # 使用DeepSeek官方API获取模型列表
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json"
            }
            
            models_url = f"{api_url}/models"
            response = httpx.get(models_url, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                data = response.json()
                if "data" in data:
                    for model in data["data"]:
                        model_id = model.get("id")
                        if model_id:
                            # 使用原始模型ID作为标签
                            models.append({"value": model_id, "label": model_id})
            else:
                # API调用失败，使用备用模型列表
                models = [
                    {"value": "deepseek-chat", "label": "deepseek-chat"},
                    {"value": "deepseek-reasoner", "label": "deepseek-reasoner"}
                ]
                
        elif "openai" in api_url.lower():
            # OpenAI模型列表
            models = [
                {"value": "gpt-4", "label": "GPT-4"},
                {"value": "gpt-3.5-turbo", "label": "GPT-3.5"},
                {"value": "gpt-4o", "label": "GPT-4o"}
            ]
        elif "anthropic" in api_url.lower():
            # Anthropic模型列表
            models = [
                {"value": "claude-3-opus-20240229", "label": "Claude 3 Opus"},
                {"value": "claude-3-sonnet-20240229", "label": "Claude 3 Sonnet"},
                {"value": "claude-3-haiku-20240307", "label": "Claude 3 Haiku"}
            ]
        elif "baidu" in api_url.lower() or "ernie" in api_url.lower():
            # 百度文心一言模型列表
            models = [
                {"value": "ernie-bot", "label": "文心一言"},
                {"value": "ernie-bot-turbo", "label": "文心一言 Turbo"},
                {"value": "ernie-bot-4", "label": "文心一言 4.0"}
            ]
        elif "xinghuo" in api_url.lower() or "iflytek" in api_url.lower():
            # 讯飞星火模型列表
            models = [
                {"value": "spark", "label": "讯飞星火"},
                {"value": "spark-lite", "label": "讯飞星火 Lite"},
                {"value": "spark-pro", "label": "讯飞星火 Pro"}
            ]
        else:
            # 默认模型列表
            models = [
                {"value": "deepseek-chat", "label": "深度搜寻聊天"},
                {"value": "gpt-3.5-turbo", "label": "GPT-3.5"},
                {"value": "claude-3-sonnet-20240229", "label": "Claude 3"}
            ]
            
    except Exception as e:
        print(f"获取模型列表失败: {str(e)}")
        # 发生错误时使用备用模型列表
        models = [
            {"value": "deepseek-chat", "label": "深度搜寻聊天"}
        ]
    
    return {"models": models}


@router.post("/backup")
def create_backup(
    current_user: User = Depends(get_current_user)
):
    """创建数据库备份"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    result = backup_service.create_backup()
    
    if result["success"]:
        # 清理旧备份
        backup_service.cleanup_old_backups(keep_count=7)
        
        return {
            "message": "备份创建成功",
            "backup": result
        }
    else:
        raise HTTPException(status_code=500, detail=f"备份创建失败: {result.get('error', '未知错误')}")


@router.get("/backups")
def get_backup_list(
    current_user: User = Depends(get_current_user)
):
    """获取备份文件列表"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    backups = backup_service.get_backup_list()
    
    # 转换文件大小为易读格式
    for backup in backups:
        size = backup["size"]
        if size < 1024:
            backup["size_text"] = f"{size} B"
        elif size < 1024 * 1024:
            backup["size_text"] = f"{size / 1024:.2f} KB"
        else:
            backup["size_text"] = f"{size / (1024 * 1024):.2f} MB"
    
    return {"backups": backups}


@router.get("/backup/{filename}")
def download_backup(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """下载备份文件"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    backup_path = backup_service.download_backup(filename)
    
    if backup_path:
        from fastapi.responses import FileResponse
        return FileResponse(
            path=backup_path,
            filename=filename,
            media_type="application/sql"
        )
    else:
        raise HTTPException(status_code=404, detail="备份文件不存在")


@router.post("/backup/restore/{filename}")
def restore_backup(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """恢复备份"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    result = backup_service.restore_backup(filename)
    
    if result["success"]:
        return {"message": "备份恢复成功"}
    else:
        raise HTTPException(status_code=500, detail=f"备份恢复失败: {result.get('error', '未知错误')}")


@router.get("/tags")
def get_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取标签列表"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")

    from app.models.meal import Tag

    # 使用依赖注入的数据库会话
    try:
        tags = db.query(Tag).all()
        return {
            "tags": [
                {"id": tag.id, "name": tag.name, "description": tag.description}
                for tag in tags
            ]
        }
    finally:
        db.close()


# 排班管理相关API
class ScheduleCreate(BaseModel):
    staff_id: int
    schedule_date: str  # YYYY-MM-DD格式
    time_slot: str
    note: Optional[str] = None

class ScheduleUpdate(BaseModel):
    note: Optional[str] = None
    status: Optional[str] = None

@router.get("/staff-schedules")
def get_staff_schedules(
    staff_id: int = Query(..., description="配送员ID"),
    start_date: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取配送员排班列表"""
    # 管理员可以查看所有配送员的排班，配送员只能查看自己的排班
    if current_user.user_type != UserType.admin and current_user.id != staff_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from datetime import datetime
    
    start = datetime.strptime(start_date, "%Y-%m-%d").date() if start_date else None
    end = datetime.strptime(end_date, "%Y-%m-%d").date() if end_date else None
    
    schedules = staff_schedule_service.get_staff_schedules(db, staff_id, start, end)
    
    return {
        "schedules": [
            {
                "id": s.id,
                "staff_id": s.staff_id,
                "schedule_date": s.schedule_date.strftime("%Y-%m-%d"),
                "time_slot": s.time_slot,
                "status": s.status,
                "note": s.note,
                "created_at": s.created_at.isoformat()
            }
            for s in schedules
        ]
    }

@router.post("/staff-schedules")
def create_staff_schedule(
    schedule_data: ScheduleCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建排班记录"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    from datetime import datetime
    
    schedule_date = datetime.strptime(schedule_data.schedule_date, "%Y-%m-%d").date()
    
    try:
        schedule = staff_schedule_service.create_schedule(
            db,
            staff_id=schedule_data.staff_id,
            schedule_date=schedule_date,
            time_slot=schedule_data.time_slot,
            note=schedule_data.note
        )
        
        return {
            "id": schedule.id,
            "staff_id": schedule.staff_id,
            "schedule_date": schedule.schedule_date.strftime("%Y-%m-%d"),
            "time_slot": schedule.time_slot,
            "status": schedule.status,
            "note": schedule.note
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        if "duplicate key" in str(e).lower():
            raise HTTPException(status_code=400, detail="该日期和时间段已存在排班记录")
        raise HTTPException(status_code=400, detail=str(e))

@router.put("/staff-schedules/{schedule_id}")
def update_staff_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新排班记录"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    schedule = staff_schedule_service.update_schedule(
        db,
        schedule_id,
        note=schedule_data.note,
        status=schedule_data.status
    )
    
    if not schedule:
        raise HTTPException(status_code=404, detail="排班记录不存在")
    
    return {
        "id": schedule.id,
        "staff_id": schedule.staff_id,
        "schedule_date": schedule.schedule_date.strftime("%Y-%m-%d"),
        "time_slot": schedule.time_slot,
        "status": schedule.status,
        "note": schedule.note
    }

@router.delete("/staff-schedules/{schedule_id}")
def delete_staff_schedule(
    schedule_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除排班记录"""
    if current_user.user_type != UserType.admin:
        raise HTTPException(status_code=403, detail="权限不足")
    
    success = staff_schedule_service.delete_schedule(db, schedule_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="排班记录不存在")
    
    return {"message": "排班记录删除成功"}

@router.get("/staff-schedules/month")
def get_month_schedules(
    staff_id: int = Query(..., description="配送员ID"),
    year: int = Query(..., description="年份"),
    month: int = Query(..., description="月份"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取月度排班记录"""
    # 管理员可以查看所有配送员的排班，配送员只能查看自己的排班
    if current_user.user_type != UserType.admin and current_user.id != staff_id:
        raise HTTPException(status_code=403, detail="权限不足")
    
    print(f"获取月度排班 - staff_id={staff_id}, year={year}, month={month}")
    
    schedules = staff_schedule_service.get_month_schedules(db, staff_id, year, month)
    
    print(f"获取到的排班记录数: {len(schedules)}")
    for s in schedules:
        print(f"  - id={s.id}, date={s.schedule_date}, slot={s.time_slot}, status={s.status}")
    
    response_data = {
        "schedules": [
            {
                "id": s.id,
                "staff_id": s.staff_id,
                "schedule_date": s.schedule_date.strftime("%Y-%m-%d"),
                "time_slot": s.time_slot,
                "status": s.status,
                "note": s.note
            }
            for s in schedules
        ]
    }
    
    return response_data