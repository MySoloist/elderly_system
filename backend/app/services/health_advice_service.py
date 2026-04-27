from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from app.models.health_record import HealthRecord
from app.models.user import ElderlyProfile
from app.models.meal import Meal, Tag
from app.services.ai_service import AIService


class HealthAdviceService:
    @staticmethod
    async def get_health_advice(db: Session, elderly_id: int) -> str:
        """获取老人的AI健康建议"""
        # 获取老人的基本信息
        elderly_profile = db.query(ElderlyProfile).filter(
            ElderlyProfile.user_id == elderly_id
        ).first()
        
        # 获取最新的健康记录
        latest_record = db.query(HealthRecord).filter(
            HealthRecord.elderly_id == elderly_id
        ).order_by(HealthRecord.recorded_at.desc()).first()
        
        if not latest_record and not elderly_profile:
            return "暂无健康数据，请先录入健康信息"
        
        # 获取所有可用的餐品及其标签
        meals = db.query(Meal).options(
            joinedload(Meal.tag)
        ).filter(
            Meal.status == 'available'
        ).all()
        
        # 准备健康数据
        health_data = {}
        
        if latest_record:
            health_data.update({
                "height": latest_record.height,
                "weight": latest_record.weight,
                "blood_pressure": latest_record.blood_pressure,
                "blood_sugar": latest_record.blood_sugar,
                "allergies": latest_record.allergies,
                "medications": latest_record.medications,
                "doctor_advice": latest_record.doctor_advice
            })
        
        if elderly_profile:
            health_data.update({
                "dietary_preferences": elderly_profile.dietary_preferences
            })
        
        # 准备餐品数据
        meals_data = []
        for meal in meals:
            meal_info = {
                "id": meal.id,
                "name": meal.name,
                "description": meal.description,
                "price": float(meal.price),
                "special_tag": meal.special_tag,
                "tag_name": meal.tag.name if meal.tag else None,
                "tag_description": meal.tag.description if meal.tag else None
            }
            meals_data.append(meal_info)
        
        health_data["meals"] = meals_data
        
        # 调用AI服务生成健康建议
        ai_service = AIService()
        return await ai_service.generate_health_advice(health_data)
