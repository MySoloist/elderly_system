from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.meal import Meal, Favorite


class MealService:
    def get_meals(self, db: Session, category: Optional[str] = None, 
                 category_id: Optional[int] = None, 
                 tag_id: Optional[int] = None,
                 tag: Optional[str] = None,
                 skip: int = 0, limit: int = 20):
        query = db.query(Meal)
        
        # 处理category参数
        if category:
            from app.models.meal import Category
            category_obj = db.query(Category).filter(Category.name == category).first()
            if category_obj:
                query = query.filter(Meal.category_id == category_obj.id)
        
        # 处理category_id参数
        if category_id:
            query = query.filter(Meal.category_id == category_id)
        
        # 处理tag_id参数
        if tag_id:
            query = query.filter(Meal.tag_id == tag_id)
        
        # 处理tag参数（按标签名称筛选）
        if tag:
            from app.models.meal import Tag
            tag_obj = db.query(Tag).filter(Tag.name == tag).first()
            if tag_obj:
                query = query.filter(Meal.tag_id == tag_obj.id)
            
        return query.offset(skip).limit(limit).all()
    
    def get_meal(self, db: Session, meal_id: int):
        return db.query(Meal).filter(Meal.id == meal_id).first()
    
    def create_meal(self, db: Session, name: str, description: str, price: float, 
                   category: str, image_url: Optional[str] = None, nutrition: Optional[List[str]] = None):
        # 查找或创建分类
        from app.models.meal import Category, Tag
        category_obj = db.query(Category).filter(Category.name == category).first()
        if not category_obj:
            category_obj = Category(name=category)
            db.add(category_obj)
            db.commit()
            db.refresh(category_obj)
        
        # 处理标签
        tag_id = None
        special_tag = None
        
        if nutrition and len(nutrition) > 0:
            # 查找第一个标签
            tag_obj = db.query(Tag).filter(Tag.name == nutrition[0]).first()
            if tag_obj:
                tag_id = tag_obj.id
            
            # 如果有多个标签，用逗号分隔存储到special_tag
            if len(nutrition) > 1:
                special_tag = ','.join(nutrition)
        
        meal = Meal(
            name=name,
            description=description,
            price=price,
            category_id=category_obj.id,
            tag_id=tag_id,
            special_tag=special_tag,
            image_url=image_url
        )
        db.add(meal)
        db.commit()
        db.refresh(meal)
        return meal
    
    def update_meal(self, db: Session, meal_id: int, **kwargs):
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if meal:
            # 处理分类更新
            if 'category' in kwargs:
                category_name = kwargs.pop('category')
                from app.models.meal import Category
                category_obj = db.query(Category).filter(Category.name == category_name).first()
                if category_obj:
                    meal.category_id = category_obj.id
            
            # 处理标签更新
            if 'nutrition' in kwargs:
                nutrition = kwargs.pop('nutrition')
                if nutrition and len(nutrition) > 0:
                    from app.models.meal import Tag
                    # 查找第一个标签
                    tag_obj = db.query(Tag).filter(Tag.name == nutrition[0]).first()
                    if tag_obj:
                        meal.tag_id = tag_obj.id
                    
                    # 如果有多个标签，用逗号分隔存储到special_tag
                    if len(nutrition) > 1:
                        meal.special_tag = ','.join(nutrition)
                    else:
                        meal.special_tag = None
            else:
                # 如果没有提供nutrition，保持原样
                pass
            
            # 更新其他字段
            for key, value in kwargs.items():
                setattr(meal, key, value)
            
            db.commit()
            db.refresh(meal)
        return meal
    
    def delete_meal(self, db: Session, meal_id: int):
        meal = db.query(Meal).filter(Meal.id == meal_id).first()
        if meal:
            db.delete(meal)
            db.commit()
            return True
        return False
    
    def add_favorite(self, db: Session, user_id: int, user_type: str, meal_id: int):
        """添加收藏（支持老人和家属）"""
        favorite = Favorite(user_id=user_id, user_type=user_type, meal_id=meal_id)
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        return favorite
    
    def remove_favorite(self, db: Session, user_id: int, user_type: str, meal_id: int):
        """取消收藏（支持老人和家属）"""
        favorite = db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.user_type == user_type,
            Favorite.meal_id == meal_id
        ).first()
        if favorite:
            db.delete(favorite)
            db.commit()
            return True
        return False
    
    def get_user_favorites(self, db: Session, user_id: int, user_type: str):
        """获取用户的收藏列表（支持老人和家属）"""
        from sqlalchemy.orm import joinedload
        return db.query(Favorite).options(
            joinedload(Favorite.meal).joinedload(Meal.category)
        ).filter(
            Favorite.user_id == user_id,
            Favorite.user_type == user_type
        ).all()
    
    def check_favorite(self, db: Session, user_id: int, user_type: str, meal_id: int):
        """检查用户是否已收藏某餐品"""
        return db.query(Favorite).filter(
            Favorite.user_id == user_id,
            Favorite.user_type == user_type,
            Favorite.meal_id == meal_id
        ).first() is not None


meal_service = MealService()
