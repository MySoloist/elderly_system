import os
import httpx
from typing import Dict, Any


class AIService:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL")
        self.model = os.getenv("DEEPSEEK_MODEL")
    
    async def generate_health_advice(self, health_data: Dict[str, Any]) -> str:
        """基于健康数据生成AI健康建议"""
        # 如果没有配置API密钥，返回错误信息
        if not self.api_key or not self.api_url or not self.model:
            return "AI服务未配置，请联系管理员配置DeepSeek API密钥"
        
        # 构建提示词
        meals_data = health_data.get('meals', [])
        meals_info = ""
        if meals_data:
            meals_info = "可用餐品：\n"
            for meal in meals_data:
                meals_info += f"- {meal.get('name', '未知')}"
                if meal.get('tag_name'):
                    meals_info += f"（{meal.get('tag_name')}）"
                if meal.get('description'):
                    meals_info += f": {meal.get('description')}"
                meals_info += "\n"
        
        prompt = f"""
基于以下老人的健康数据和可用餐品，生成专业的健康建议和餐品推荐：

健康数据：
- 身高：{health_data.get('height', '未知')} cm
- 体重：{health_data.get('weight', '未知')} kg
- 血压：{health_data.get('blood_pressure', '未知')}
- 血糖：{health_data.get('blood_sugar', '未知')} mmol/L
- 饮食偏好：{health_data.get('dietary_preferences', '无')}
- 过敏史：{health_data.get('allergies', '无')}
- 用药情况：{health_data.get('medications', '无')}
- 医生建议：{health_data.get('doctor_advice', '无')}

{meals_info}

请先复述以上健康数据，然后提供：
1. 健康状况分析
2. 饮食建议（适合老年人的营养均衡饮食）
3. 生活习惯建议    
4. 需要注意的健康风险
5. 餐品推荐（根据健康数据和饮食偏好，从可用餐品中推荐2-3个最适合的餐品，并说明推荐理由）
6. 简单易懂的健康提示

要求：语言亲切友好，建议具体可行，避免使用专业术语。
     你写的这些内容是给老人的家属看的，不是给老人看的，请你注意一下人称的称呼。
        """
        
        try:
            # 调用DeepSeek API
            print(f"正在调用DeepSeek API...")
            print(f"API URL: {self.api_url}")
            print(f"Model: {self.model}")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                print(f"API响应状态码: {response.status_code}")
                
                if response.status_code == 200:
                    result = response.json()
                    print("API调用成功")
                    return result["choices"][0]["message"]["content"]
                else:
                    error_detail = response.text
                    print(f"API调用失败: {error_detail}")
                    return f"AI服务调用失败，状态码：{response.status_code}，详情：{error_detail}"
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"AI服务调用异常: {str(e)}")
            print(f"异常堆栈:\n{error_trace}")
            return f"AI服务调用失败：{str(e)}"
    
    async def generate_meal_recommendations(self, health_data: Dict[str, Any], meals: list) -> str:
        """使用AI生成餐品推荐"""
        # 如果没有配置API密钥，返回错误信息
        if not self.api_key or not self.api_url or not self.model:
            return "AI服务未配置"
        
        # 构建餐品信息
        meals_info = "可用餐品：\n"
        for meal in meals:
            meal_info = f"- ID: {meal.id}, 名称：{meal.name}"
            if meal.tag:
                meal_info += f"（{meal.tag.name}）"
            if meal.description:
                meal_info += f": {meal.description}"
            meals_info += meal_info + "\n"
        
        # 构建提示词
        prompt = f"""
你是一位专业的营养师AI，基于老人的健康数据和饮食偏好，从可用餐品中推荐最适合的餐品。

老人健康数据：
- 身高：{health_data.get('height', '未知')} cm
- 体重：{health_data.get('weight', '未知')} kg
- 血压：{health_data.get('blood_pressure', '未知')}
- 血糖：{health_data.get('blood_sugar', '未知')} mmol/L
- 饮食偏好：{health_data.get('dietary_preferences', '无')}
- 过敏史：{health_data.get('allergies', '无')}
- 用药情况：{health_data.get('medications', '无')}
- 医生建议：{health_data.get('doctor_advice', '无')}

{meals_info}

请根据以上健康数据和饮食偏好，从可用餐品中推荐4个最适合的餐品，并为每个餐品提供详细的推荐理由。
请按照以下JSON格式返回：
[
    {{
        "meal_id": 1,
        "reason": "详细的推荐理由，说明为什么推荐这个餐品"
    }},
    {{
        "meal_id": 2,
        "reason": "详细的推荐理由，说明为什么推荐这个餐品"
    }}
]

注意：
1. 必须从可用餐品中选择
2. 推荐要考虑健康状况（血压、血糖等）
3. 要考虑饮食偏好
4. 推荐理由要详细具体，说明为什么这个餐品适合该老人
5. 只返回JSON格式，不要返回其他文字
"""
        
        try:
            # 调用DeepSeek API
            print(f"正在调用DeepSeek API进行餐品推荐...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    print(f"AI推荐结果: {ai_response}")
                    return ai_response
                else:
                    error_detail = response.text
                    print(f"AI推荐失败: {error_detail}")
                    return "AI推荐失败"
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"AI推荐异常: {str(e)}")
            print(f"异常堆栈:\n{error_trace}")
            return "AI推荐失败"
    
    async def generate_ai_response(self, query: str, user_type: str, db=None, user_id=None) -> str:
        """生成AI回复"""
        # 如果没有配置API密钥，返回错误信息
        if not self.api_key or not self.api_url or not self.model:
            return "AI服务未配置，请联系管理员配置DeepSeek API密钥"
        
        # 获取系统数据
        system_data = ""
        if db:
            try:
                # 1. 餐品数据
                from app.models import Meal
                # 打印调试信息
                print("获取系统中的餐品菜单")
                meals = db.query(Meal).filter(Meal.status == "available").all()
                print(f"找到 {len(meals)} 个可用餐品")
                if meals:
                    system_data += "\n\n系统中的餐品菜单：\n"
                    for meal in meals:
                        system_data += f"- {meal.name}：¥{meal.price}，{meal.description}\n"
                else:
                    system_data += "\n\n系统中的餐品菜单：\n- 暂无可用餐品\n"
                
                # 2. 健康数据（如果有用户ID）
                if user_id:
                    from app.models import HealthRecord, ElderlyProfile
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的健康记录")
                    # 获取老人健康记录
                    health_record = db.query(HealthRecord).filter(
                        HealthRecord.elderly_id == user_id
                    ).order_by(HealthRecord.recorded_at.desc()).first()
                    print(f"找到健康记录：{health_record is not None}")
                    if health_record:
                        system_data += "\n\n老人健康数据：\n"
                        system_data += f"- 身高：{health_record.height or '未知'} cm\n"
                        system_data += f"- 体重：{health_record.weight or '未知'} kg\n"
                        system_data += f"- 血压：{health_record.blood_pressure or '未知'}\n"
                        system_data += f"- 血糖：{health_record.blood_sugar or '未知'} mmol/L\n"
                        system_data += f"- 过敏史：{health_record.allergies or '无'}\n"
                        system_data += f"- 用药情况：{health_record.medications or '无'}\n"
                    else:
                        system_data += "\n\n老人健康数据：\n- 暂无健康记录\n"
                    # 获取老人档案
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的老人档案")
                    elderly_profile = db.query(ElderlyProfile).filter(
                        ElderlyProfile.user_id == user_id
                    ).first()
                    print(f"找到老人档案：{elderly_profile is not None}")
                    if elderly_profile:
                        system_data += "\n\n老人档案：\n"
                        system_data += f"- 姓名：{elderly_profile.name or '未知'}\n"
                        system_data += f"- 年龄：{elderly_profile.age or '未知'}\n"
                        system_data += f"- 性别：{elderly_profile.gender or '未知'}\n"
                        system_data += f"- 电话：{elderly_profile.phone or '未知'}\n"
                        system_data += f"- 地址：{elderly_profile.address or '未知'}\n"
                        system_data += f"- 饮食偏好：{elderly_profile.dietary_preferences or '无'}\n"
                        # 获取社区信息
                        if elderly_profile.community:
                            system_data += f"- 所在社区：{elderly_profile.community.name or '未知'}\n"
                        # 获取健康标签信息
                        if elderly_profile.health_tag:
                            system_data += f"- 健康标签：{elderly_profile.health_tag.name or '未知'}\n"
                    else:
                        system_data += "\n\n老人档案：\n- 暂无老人档案\n"
                
                # 3. 历史订单数据（如果有用户ID）
                if user_id:
                    from app.models import Order, OrderItem
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的历史订单")
                    orders = db.query(Order).filter(
                        Order.elderly_id == user_id
                    ).order_by(Order.created_at.desc()).limit(5).all()
                    print(f"找到 {len(orders)} 个历史订单")
                    if orders:
                        system_data += "\n\n最近的历史订单：\n"
                        for order in orders:
                            order_items = db.query(OrderItem).filter(
                                OrderItem.order_id == order.id
                            ).all()
                            items_str = ", ".join([f"{item.meal.name} x{item.quantity}" for item in order_items if item.meal])
                            # 添加订单创建时间
                            created_time = order.created_at.strftime('%Y-%m-%d %H:%M:%S') if order.created_at else '未知'
                            system_data += f"- 订单号：{order.id}，下单时间：{created_time}，金额：¥{order.total_amount}，状态：{order.status}，餐品：{items_str}\n"
                    else:
                        system_data += "\n\n最近的历史订单：\n- 暂无历史订单\n"
                
                # 4. 公告信息
                from app.models import Announcement
                announcements = db.query(Announcement).filter(
                    Announcement.status == "active"
                ).order_by(Announcement.created_at.desc()).limit(3).all()
                if announcements:
                    system_data += "\n\n最新公告：\n"
                    for announcement in announcements:
                        system_data += f"- {announcement.title}：{announcement.content[:50]}...\n"
                
                # 5. 社区信息
                from app.models import Community
                communities = db.query(Community).filter(
                    Community.status == "active"
                ).all()
                if communities:
                    system_data += "\n\n服务社区：\n"
                    for community in communities:
                        system_data += f"- {community.name}：{community.address}\n"
                
                # 6. 餐品分类和标签
                from app.models import Category, Tag
                categories = db.query(Category).all()
                if categories:
                    system_data += "\n\n餐品分类：\n"
                    for category in categories:
                        system_data += f"- {category.name}\n"
                
                tags = db.query(Tag).all()
                if tags:
                    system_data += "\n\n餐品标签：\n"
                    for tag in tags:
                        system_data += f"- {tag.name}\n"
                
                # 7. 健康标签
                from app.models import HealthTag
                health_tags = db.query(HealthTag).all()
                if health_tags:
                    system_data += "\n\n健康标签：\n"
                    for tag in health_tags:
                        system_data += f"- {tag.name}：{tag.description[:30]}...\n"
                
                # 8. 健康提醒
                if user_id:
                    from app.models import HealthReminder
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的健康提醒")
                    # 使用正确的字段名 receiver_id，而不是 elderly_id
                    health_reminders = db.query(HealthReminder).filter(
                        HealthReminder.receiver_id == user_id
                    ).order_by(HealthReminder.scheduled_time.desc()).limit(5).all()
                    print(f"找到 {len(health_reminders)} 个健康提醒")
                    if health_reminders:
                        system_data += "\n\n健康提醒：\n"
                        for reminder in health_reminders:
                            reminder_time = reminder.scheduled_time.strftime('%Y-%m-%d %H:%M') if reminder.scheduled_time else '未知'
                            # 使用正确的字段名 content，而不是 description
                            system_data += f"- {reminder.reminder_type}：{reminder_time}，{reminder.content[:30]}...\n"
                    else:
                        system_data += "\n\n健康提醒：\n- 暂无健康提醒\n"
                
                # 9. 收藏的餐品
                if user_id:
                    from app.models import Favorite, Meal
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的收藏餐品")
                    # 使用正确的字段名 user_id，而不是 elderly_id
                    favorites = db.query(Favorite).filter(
                        Favorite.user_id == user_id,
                        Favorite.user_type == "elderly"
                    ).all()
                    print(f"找到 {len(favorites)} 个收藏餐品")
                    if favorites:
                        system_data += "\n\n您收藏的餐品：\n"
                        for favorite in favorites:
                            if favorite.meal:
                                print(f"收藏餐品：{favorite.meal.name}")
                                system_data += f"- {favorite.meal.name}：¥{favorite.meal.price}，{favorite.meal.description[:30]}...\n"
                    else:
                        system_data += "\n\n您收藏的餐品：\n- 暂无收藏餐品\n"
                
                # 10. 餐品评价
                if user_id:
                    from app.models import Review
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的餐品评价")
                    reviews = db.query(Review).filter(
                        Review.elderly_id == user_id
                    ).order_by(Review.created_at.desc()).limit(5).all()
                    print(f"找到 {len(reviews)} 个餐品评价")
                    if reviews:
                        system_data += "\n\n您的餐品评价：\n"
                        for review in reviews:
                            review_time = review.created_at.strftime('%Y-%m-%d %H:%M') if review.created_at else '未知'
                            system_data += f"- {review.meal.name if review.meal else '未知餐品'}：{review.rating}星，{review.content[:30]}...，{review_time}\n"
                    else:
                        system_data += "\n\n您的餐品评价：\n- 暂无餐品评价\n"
                
                # 11. 配送信息
                if user_id:
                    from app.models import Delivery, Order
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的配送信息")
                    deliveries = db.query(Delivery).join(Order).filter(
                        Order.elderly_id == user_id
                    ).order_by(Delivery.created_at.desc()).limit(5).all()
                    print(f"找到 {len(deliveries)} 个配送信息")
                    if deliveries:
                        system_data += "\n\n最近的配送信息：\n"
                        for delivery in deliveries:
                            delivery_time = delivery.created_at.strftime('%Y-%m-%d %H:%M') if delivery.created_at else '未知'
                            status = delivery.status or '未知'
                            system_data += f"- 配送单号：{delivery.id}，状态：{status}，时间：{delivery_time}\n"
                    else:
                        system_data += "\n\n最近的配送信息：\n- 暂无配送信息\n"
                
                # 12. 支付记录
                if user_id:
                    from app.models import Payment, Order
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的支付记录")
                    payments = db.query(Payment).join(Order).filter(
                        Order.elderly_id == user_id
                    ).order_by(Payment.created_at.desc()).limit(5).all()
                    print(f"找到 {len(payments)} 个支付记录")
                    if payments:
                        system_data += "\n\n最近的支付记录：\n"
                        for payment in payments:
                            payment_time = payment.created_at.strftime('%Y-%m-%d %H:%M') if payment.created_at else '未知'
                            amount = payment.amount or 0
                            status = payment.status or '未知'
                            system_data += f"- 支付金额：¥{amount}，状态：{status}，时间：{payment_time}\n"
                    else:
                        system_data += "\n\n最近的支付记录：\n- 暂无支付记录\n"
                
                # 13. 紧急呼叫记录
                if user_id:
                    from app.models import EmergencyCall
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的紧急呼叫记录")
                    emergency_calls = db.query(EmergencyCall).filter(
                        EmergencyCall.elderly_id == user_id
                    ).order_by(EmergencyCall.created_at.desc()).limit(5).all()
                    print(f"找到 {len(emergency_calls)} 个紧急呼叫记录")
                    if emergency_calls:
                        system_data += "\n\n紧急呼叫记录：\n"
                        for call in emergency_calls:
                            call_time = call.created_at.strftime('%Y-%m-%d %H:%M') if call.created_at else '未知'
                            status = call.status or '未知'
                            system_data += f"- 呼叫时间：{call_time}，状态：{status}，原因：{call.reason[:30]}...\n"
                    else:
                        system_data += "\n\n紧急呼叫记录：\n- 暂无紧急呼叫记录\n"
                
                # 14. 家属信息
                if user_id:
                    from app.models import ElderMemberRelation, MemberProfile, User
                    # 打印调试信息
                    print(f"获取用户 {user_id} 的家属信息")
                    # 使用正确的字段名 elder_id，而不是 elderly_id
                    relations = db.query(ElderMemberRelation).filter(
                        ElderMemberRelation.elder_id == user_id
                    ).all()
                    print(f"找到 {len(relations)} 个家属关系")
                    if relations:
                        system_data += "\n\n您的家属信息：\n"
                        for relation in relations:
                            # 获取家属的详细信息
                            if relation.member:
                                # 尝试从 MemberProfile 获取信息
                                member_profile = db.query(MemberProfile).filter(
                                    MemberProfile.user_id == relation.member.id
                                ).first()
                                if member_profile:
                                    member_name = member_profile.name or relation.member.username or '未知'
                                    phone = member_profile.phone or '未知'
                                else:
                                    member_name = relation.member.username or '未知'
                                    phone = '未知'
                                relation_type = relation.relationship or '未知关系'
                                system_data += f"- {member_name}（{relation_type}）：{phone}\n"
                    else:
                        system_data += "\n\n您的家属信息：\n- 暂无家属信息\n"
            except Exception as e:
                print(f"获取系统数据失败: {str(e)}")
        
        # 根据用户类型构建不同的提示词
        if user_type == "admin":
            prompt = f"""
你是一位专业的养老膳食系统管理员助手AI，请基于颐养膳食系统的业务场景，为管理员提供专业、实用的回答。

用户问题：{query}

{system_data}

请提供详细、专业的回答，包括具体的操作建议和业务流程说明。
"""
        elif user_type == "elderly":
            prompt = f"""
你是一位亲切友好的老人AI助手，请用简单易懂的语言回答老人的问题。

老人问题：{query}

{system_data}

请用亲切、耐心的语气回答，避免使用复杂的专业术语。
注意：你面对的是老人，应该使用尊敬、亲切的称呼，如"爷爷"、"奶奶"、"老人家"等，绝对不要称呼老人为"孩子"。

重要要求：
1. 如果你需要回答老人关于具体数据的问题（如收藏的餐品、历史订单、健康数据等），请基于上面提供的系统数据，列出具体的内容，不要只说数量，要列出详细信息。
2. 如果你没有相关数据，请明确告诉老人，不要编造信息。
3. 回答要具体、详细，让老人能够清楚了解情况。

如果老人询问菜单、餐品、点餐相关的问题，请基于上面提供的餐品菜单信息回答。
如果老人询问健康相关的问题，请基于上面提供的健康数据回答。
如果老人询问订单相关的问题，请基于上面提供的历史订单信息回答。
如果老人询问系统公告，请基于上面提供的公告信息回答。
如果老人询问收藏的餐品，请基于上面提供的收藏餐品信息回答，列出具体的餐品名称、价格和描述。
如果老人询问健康提醒，请基于上面提供的健康提醒信息回答，列出具体的提醒内容和时间。
如果老人询问家属信息，请基于上面提供的家属信息回答，列出具体的家属姓名、关系和联系方式。
"""
        else:
            prompt = f"""
你是一位专业的AI助手，请回答以下问题：

问题：{query}

{system_data}
"""
        
        try:
            # 调用DeepSeek API
            print(f"正在调用DeepSeek API生成AI回复...")
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.api_url}/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": self.model,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ],
                        "temperature": 0.7
                    },
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result["choices"][0]["message"]["content"]
                    print(f"AI回复生成成功")
                    return ai_response
                else:
                    error_detail = response.text
                    print(f"AI回复生成失败: {error_detail}")
                    return f"AI回复生成失败，状态码：{response.status_code}"
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"AI回复生成异常: {str(e)}")
            print(f"异常堆栈:\n{error_trace}")
            return f"AI回复生成失败：{str(e)}"
    
    def create_conversation(self, db, user_id: int, user_query: str, ai_response: str, conversation_type: str):
        """创建对话记录"""
        from app.models import AIConversation
        import uuid
        
        # 生成唯一的conversation_id
        conversation_id = str(uuid.uuid4())
        
        conversation = AIConversation(
            user_id=user_id,
            conversation_id=conversation_id,
            user_query=user_query,
            ai_response=ai_response,
            conversation_type=conversation_type
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    
    def get_user_conversations(self, db, user_id: int):
        """获取用户的对话历史"""
        from app.models import AIConversation
        
        conversations = db.query(AIConversation).filter(
            AIConversation.user_id == user_id
        ).order_by(AIConversation.created_at.desc()).all()
        
        return conversations
    

