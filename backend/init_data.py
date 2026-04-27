from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.database import SessionLocal, engine
from app.core.security import get_password_hash
from app.models import User, Meal, Order, OrderItem, ElderlyProfile, MemberProfile, DelivererProfile, AdminProfile, Category, Tag, Favorite

def init_database(force=False):
    db = SessionLocal()
    
    try:
        # 检查是否已有数据
        if db.query(User).count() > 0 and not force:
            print("数据库已有数据，跳过初始化")
            return
        
        if force:
            print("强制重新初始化数据库...")
            # 删除所有数据（按外键关系顺序）
            try:
                db.query(Favorite).delete()
                db.query(OrderItem).delete()
                db.query(Order).delete()
                
                # 尝试删除可能存在的关联表
                try:
                    db.execute(text("DELETE FROM elder_member_relations"))
                except:
                    pass
                    
                db.query(AdminProfile).delete()
                db.query(DelivererProfile).delete()
                db.query(MemberProfile).delete()
                db.query(ElderlyProfile).delete()
                db.query(Meal).delete()
                db.query(Tag).delete()
                db.query(Category).delete()
                db.query(User).delete()
                db.commit()
                print("已清空数据库")
            except Exception as e:
                db.rollback()
                print(f"清空数据库失败: {e}")
                # 如果删除失败，尝试更激进的方式
                print("尝试使用TRUNCATE命令...")
                db.execute(text("TRUNCATE TABLE users CASCADE"))
                db.commit()
                print("已使用TRUNCATE清空数据库")
        
        # 创建测试用户
        users = [
            # 老人用户
            User(
                username="elderly1",
                password_hash=get_password_hash("123456"),
                user_type="elderly",
                status="active"
            ),
            # 家属用户
            User(
                username="member1",
                password_hash=get_password_hash("123456"),
                user_type="member",
                status="active"
            ),
            # 配送员用户
            User(
                username="deliverer1",
                password_hash=get_password_hash("123456"),
                user_type="deliverer",
                status="active"
            ),
            # 管理员用户
            User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                user_type="admin",
                status="active"
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.flush()
        
        # 创建用户资料
        profiles = [
            ElderlyProfile(
                user_id=users[0].id,
                name="张奶奶",
                phone="13800138001",
                address="幸福小区3号楼2单元501室",
                dietary_preferences="低糖、低盐"
            ),
            MemberProfile(
                user_id=users[1].id,
                name="张三",
                phone="13800138002"
            ),
            DelivererProfile(
                user_id=users[2].id,
                name="李师傅",
                phone="13800138003",
                vehicle_type="电动车"
            ),
            AdminProfile(
                user_id=users[3].id,
                name="管理员",
                phone="13800138004"
            )
        ]
        
        for profile in profiles:
            db.add(profile)
        
        # 创建分类
        categories = [
            Category(name="主食", description="主食类餐品"),
            Category(name="凉菜", description="凉菜类餐品"),
            Category(name="荤菜", description="荤菜类餐品"),
            Category(name="辅食", description="辅食类餐品")
        ]
        
        for category in categories:
            db.add(category)
        
        # 创建标签
        tags = [
            Tag(name="低糖", description="低糖健康餐品"),
            Tag(name="素食", description="素食餐品"),
            Tag(name="清淡", description="清淡易消化"),
            Tag(name="高蛋白", description="高蛋白营养餐"),
            Tag(name="易消化", description="流食软食"),
            Tag(name="营养", description="营养均衡套餐")
        ]
        
        for tag in tags:
            db.add(tag)
        
        db.flush()  # 获取分类和标签的ID
        
        # 创建测试餐品
        meals = [
            Meal(
                name="营养套餐A",
                price=28.00,
                description="营养均衡的套餐，包含主食、蔬菜和蛋白质",
                category_id=categories[0].id,  # 主食分类
                tag_id=tags[5].id,  # 营养标签
                special_tag="低糖",  # 保留兼容旧逻辑
                image_url="https://example.com/images/meal1.jpg",
                status="available"
            ),
            Meal(
                name="蔬菜沙拉",
                price=18.00,
                description="新鲜蔬菜沙拉，健康低脂",
                category_id=categories[1].id,  # 凉菜分类
                tag_id=tags[1].id,  # 素食标签
                special_tag="素食",  # 保留兼容旧逻辑
                image_url="https://example.com/images/meal2.jpg",
                status="available"
            ),
            Meal(
                name="小米粥",
                price=8.00,
                description="养胃小米粥",
                category_id=categories[0].id,  # 主食分类
                tag_id=tags[2].id,  # 清淡标签
                special_tag="清淡",  # 保留兼容旧逻辑
                image_url="https://example.com/images/meal3.jpg",
                status="available"
            ),
            Meal(
                name="清蒸鱼",
                price=38.00,
                description="新鲜清蒸鱼，营养丰富",
                category_id=categories[2].id,  # 荤菜分类
                tag_id=tags[3].id,  # 高蛋白标签
                special_tag="高蛋白",  # 保留兼容旧逻辑
                image_url="https://example.com/images/meal4.jpg",
                status="available"
            ),
            Meal(
                name="鸡蛋羹",
                price=12.00,
                description="嫩滑鸡蛋羹",
                category_id=categories[3].id,  # 辅食分类
                tag_id=tags[4].id,  # 易消化标签
                special_tag="易消化",  # 保留兼容旧逻辑
                image_url="https://example.com/images/meal5.jpg",
                status="available"
            )
        ]
        
        for meal in meals:
            db.add(meal)
        
        db.commit()
        print("数据库初始化完成！")
        print(f"创建了 {len(users)} 个用户")
        print(f"创建了 {len(meals)} 个餐品")
        
    except Exception as e:
        db.rollback()
        print(f"初始化失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import sys
    force = len(sys.argv) > 1 and sys.argv[1] == "--force"
    init_database(force=force)