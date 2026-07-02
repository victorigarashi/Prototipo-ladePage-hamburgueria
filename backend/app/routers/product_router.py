from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.combo_schema import ComboResponse
from app.schemas.product_schema import ProductResponse
from app.schemas.promotion_schema import PromotionResponse
from app.services.combo_service import list_public_combos
from app.services.product_service import get_product, list_public_products
from app.services.promotion_service import list_public_promotions


router = APIRouter(tags=["Landing pública"])


@router.get("/products", response_model=list[ProductResponse])
def public_products(db: Session = Depends(get_db)):
    return list_public_products(db)


@router.get("/products/{product_id}", response_model=ProductResponse)
def public_product(product_id: int, db: Session = Depends(get_db)):
    return get_product(db, product_id, public_only=True)


@router.get("/combos", response_model=list[ComboResponse])
def public_combos(db: Session = Depends(get_db)):
    return list_public_combos(db)


@router.get("/promotions", response_model=list[PromotionResponse])
def public_promotions(db: Session = Depends(get_db)):
    return list_public_promotions(db)
