from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.health_record import HealthRecord


class HealthService:
    @staticmethod
    def get_elderly_health_records(db: Session, elderly_id: int) -> List[HealthRecord]:
        """获取老年人的健康记录列表"""
        return db.query(HealthRecord).filter(
            HealthRecord.elderly_id == elderly_id
        ).order_by(HealthRecord.recorded_at.desc()).all()
    
    @staticmethod
    def get_health_record_by_id(db: Session, record_id: int) -> Optional[HealthRecord]:
        """根据ID获取健康记录"""
        return db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
    
    @staticmethod
    def create_health_record(
        db: Session,
        elderly_id: int,
        height: Optional[float] = None,
        weight: Optional[float] = None,
        blood_pressure: Optional[str] = None,
        blood_sugar: Optional[float] = None,
        allergies: Optional[str] = None,
        medications: Optional[str] = None,
        doctor_advice: Optional[str] = None,
        created_by: Optional[int] = None
    ) -> HealthRecord:
        """创建健康记录"""
        health_record = HealthRecord(
            elderly_id=elderly_id,
            height=height,
            weight=weight,
            blood_pressure=blood_pressure,
            blood_sugar=blood_sugar,
            allergies=allergies,
            medications=medications,
            doctor_advice=doctor_advice,
            created_by=created_by
        )
        db.add(health_record)
        db.commit()
        db.refresh(health_record)
        return health_record
    
    @staticmethod
    def update_health_record(
        db: Session,
        record_id: int,
        height: Optional[float] = None,
        weight: Optional[float] = None,
        blood_pressure: Optional[str] = None,
        blood_sugar: Optional[float] = None,
        allergies: Optional[str] = None,
        medications: Optional[str] = None,
        doctor_advice: Optional[str] = None
    ) -> Optional[HealthRecord]:
        """更新健康记录"""
        health_record = db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
        if health_record:
            if height is not None:
                health_record.height = height
            if weight is not None:
                health_record.weight = weight
            if blood_pressure is not None:
                health_record.blood_pressure = blood_pressure
            if blood_sugar is not None:
                health_record.blood_sugar = blood_sugar
            if allergies is not None:
                health_record.allergies = allergies
            if medications is not None:
                health_record.medications = medications
            if doctor_advice is not None:
                health_record.doctor_advice = doctor_advice
            db.commit()
            db.refresh(health_record)
        return health_record
    
    @staticmethod
    def delete_health_record(db: Session, record_id: int) -> bool:
        """删除健康记录"""
        health_record = db.query(HealthRecord).filter(HealthRecord.id == record_id).first()
        if health_record:
            db.delete(health_record)
            db.commit()
            return True
        return False
