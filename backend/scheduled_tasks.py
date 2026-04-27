import time
import schedule
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.order import Order

def process_scheduled_orders():
    """处理预定订单，将到时间的预定订单转换为待接单状态"""
    db: Session = SessionLocal()
    try:
        now = datetime.now(timezone.utc)
        
        # 查找所有状态为pending_schedule且预定时间已到的订单
        scheduled_orders = db.query(Order).filter(
            Order.status == "pending_schedule",
            Order.scheduled_time <= now
        ).all()
        
        print(f"找到 {len(scheduled_orders)} 个需要处理的预定订单")
        
        for order in scheduled_orders:
            # 更新订单状态为待接单
            order.status = "pending_accept"
            print(f"订单 {order.id} 已从 pending_schedule 转换为 pending_accept")
        
        db.commit()
        print("预定订单状态更新完成")
        
    except Exception as e:
        print(f"处理预定订单时出错: {e}")
        db.rollback()
    finally:
        db.close()

def start_scheduled_tasks():
    """启动定时任务"""
    # 每分钟检查一次预定订单
    schedule.every(1).minutes.do(process_scheduled_orders)
    
    print("定时任务已启动，每分钟检查一次预定订单")
    
    # 立即执行一次
    process_scheduled_orders()
    
    # 运行定时任务
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    start_scheduled_tasks()
