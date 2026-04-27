from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date, datetime

from app.models.staff_schedule import StaffSchedule

class StaffScheduleService:
    def create_schedule(self, db: Session, staff_id: int, schedule_date: date, time_slot: str, note: Optional[str] = None) -> StaffSchedule:
        """创建排班记录"""
        # 检查是否已存在相同的排班记录
        existing_schedule = db.query(StaffSchedule).filter(
            StaffSchedule.staff_id == staff_id,
            StaffSchedule.schedule_date == schedule_date,
            StaffSchedule.time_slot == time_slot
        ).first()
        
        if existing_schedule:
            raise ValueError(f"该配送员在{schedule_date} {time_slot}时间段已有排班安排")
        
        schedule = StaffSchedule(
            staff_id=staff_id,
            schedule_date=schedule_date,
            time_slot=time_slot,
            note=note
        )
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    
    def get_staff_schedules(self, db: Session, staff_id: int, start_date: Optional[date] = None, end_date: Optional[date] = None) -> List[StaffSchedule]:
        """获取配送员的排班记录"""
        query = db.query(StaffSchedule).filter(StaffSchedule.staff_id == staff_id)
        
        if start_date:
            query = query.filter(StaffSchedule.schedule_date >= start_date)
        if end_date:
            query = query.filter(StaffSchedule.schedule_date<= end_date)
        
        return query.order_by(StaffSchedule.schedule_date, StaffSchedule.time_slot).all()
    
    def get_schedule_by_id(self, db: Session, schedule_id: int) -> Optional[StaffSchedule]:
        """根据ID获取排班记录"""
        return db.query(StaffSchedule).filter(StaffSchedule.id == schedule_id).first()
    
    def update_schedule(self, db: Session, schedule_id: int, note: Optional[str] = None, status: Optional[str] = None) -> Optional[StaffSchedule]:
        """更新排班记录"""
        schedule = self.get_schedule_by_id(db, schedule_id)
        if schedule:
            if note is not None:
                schedule.note = note
            if status is not None:
                schedule.status = status
            db.commit()
            db.refresh(schedule)
        return schedule
    
    def delete_schedule(self, db: Session, schedule_id: int) -> bool:
        """删除排班记录"""
        schedule = self.get_schedule_by_id(db, schedule_id)
        if schedule:
            db.delete(schedule)
            db.commit()
            return True
        return False
    
    def get_month_schedules(self, db: Session, staff_id: int, year: int, month: int) -> List[StaffSchedule]:
        """获取指定月份的排班记录"""
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
        
        return self.get_staff_schedules(db, staff_id, start_date, end_date)
    
    def get_week_schedules(self, db: Session, staff_id: int, start_date: date) -> List[StaffSchedule]:
        """获取指定周的排班记录"""
        end_date = date(start_date.year, start_date.month, start_date.day + 6)
        return self.get_staff_schedules(db, staff_id, start_date, end_date)

staff_schedule_service = StaffScheduleService()
