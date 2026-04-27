from app.core.database import get_db
from app.models.order import Order, Payment

# 获取数据库会话
db = next(get_db())

# 查询所有订单，查看payment_status
orders = db.query(Order).all()

print(f"总订单数: {len(orders)}")
print("\n订单详情:")
for order in orders:
    print(f"订单ID: {order.id}, 状态: {order.status}, 支付状态: {order.payment_status}, 支付方式: {order.payment_method}")

# 找出支付状态为已支付的订单
paid_orders = db.query(Order).filter(Order.payment_status == 'paid').all()
print(f"\n支付状态为已支付的订单数: {len(paid_orders)}")

# 为每个支付状态为已完成的订单创建支付记录
for order in paid_orders:
    # 检查是否已经有支付记录
    existing_payment = db.query(Payment).filter(Payment.order_id == order.id).first()
    if existing_payment:
        print(f"订单 {order.id} 已有支付记录，跳过")
        continue
    
    # 创建支付记录
    payment = Payment(
        order_id=order.id,
        payment_method=order.payment_method or '微信支付',
        amount=order.total_amount,
        transaction_id=f'TXN{order.id:06d}',
        status='completed',
        created_at=order.created_at
    )
    db.add(payment)
    print(f"为订单 {order.id} 创建支付记录，支付方式: {payment.payment_method}")

# 提交事务
db.commit()
print("\n支付记录创建完成")
