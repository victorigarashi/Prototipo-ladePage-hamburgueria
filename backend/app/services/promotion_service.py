from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.promotion_model import Promotion
from app.schemas.promotion_schema import PromotionCreate, PromotionUpdate


def list_public_promotions(db: Session) -> list[Promotion]:
    return db.query(Promotion).filter(Promotion.is_active.is_(True)).order_by(Promotion.created_at.desc()).all()


def list_admin_promotions(db: Session) -> list[Promotion]:
    return db.query(Promotion).order_by(Promotion.created_at.desc()).all()


def get_promotion(db: Session, promotion_id: int) -> Promotion:
    promotion = db.get(Promotion, promotion_id)
    if not promotion:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Promoção não encontrada.")
    return promotion


def create_promotion(db: Session, payload: PromotionCreate) -> Promotion:
    promotion = Promotion(**payload.model_dump())
    db.add(promotion)
    db.commit()
    db.refresh(promotion)
    return promotion


def update_promotion(db: Session, promotion_id: int, payload: PromotionUpdate) -> Promotion:
    promotion = get_promotion(db, promotion_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(promotion, field, value)
    db.commit()
    db.refresh(promotion)
    return promotion


def delete_promotion(db: Session, promotion_id: int) -> None:
    promotion = get_promotion(db, promotion_id)
    db.delete(promotion)
    db.commit()
