from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.review import Review
from app.models.order import Order, OrderItem


class ReviewService:
    def get_reviews(self, db: Session, skip: int = 0, limit: int = 20):
        """获取评价列表"""
        # 优先显示待审核的评价，然后按创建时间降序排列
        from sqlalchemy import case
        from sqlalchemy.orm import joinedload
        return db.query(Review).options(
            joinedload(Review.elderly),
            joinedload(Review.deliverer),
            joinedload(Review.order).joinedload(Order.items).joinedload(OrderItem.meal)
        ).order_by(
            case(
                (Review.status == 'pending', 0),
                else_=1
            ),
            Review.created_at.desc()
        ).offset(skip).limit(limit).all()
    
    def get_review(self, db: Session, review_id: int):
        """获取单个评价详情"""
        return db.query(Review).filter(Review.id == review_id).first()
    
    def create_review(self, db: Session, order_id: Optional[int], elderly_id: int, 
                    rating: int, content: str, status: str = "approved", images: Optional[List[str]] = None, reviewer_type: str = "elderly", deliverer_id: Optional[int] = None):
        """创建评价"""
        review = Review(
            order_id=order_id,
            elderly_id=elderly_id,
            rating=rating,
            content=content,
            status=status,
            images=images,
            reviewer_type=reviewer_type,
            deliverer_id=deliverer_id
        )
        db.add(review)
        db.commit()
        db.refresh(review)
        return review
    
    def update_review(self, db: Session, review_id: int, **kwargs):
        """更新评价"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            for key, value in kwargs.items():
                setattr(review, key, value)
            db.commit()
            db.refresh(review)
        return review
    
    def delete_review(self, db: Session, review_id: int):
        """删除评价"""
        review = db.query(Review).filter(Review.id == review_id).first()
        if review:
            db.delete(review)
            db.commit()
            return True
        return False


review_service = ReviewService()
