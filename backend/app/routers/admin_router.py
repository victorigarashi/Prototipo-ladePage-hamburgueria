from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.category_schema import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.combo_schema import ComboCreate, ComboResponse, ComboUpdate
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.schemas.promotion_schema import PromotionCreate, PromotionResponse, PromotionUpdate
from app.security import require_admin
from app.services.category_service import create_category, delete_category, list_categories, update_category
from app.services.combo_service import create_combo, delete_combo, list_admin_combos, toggle_combo_active, toggle_combo_available, update_combo
from app.services.product_service import create_product, delete_product, list_admin_products, toggle_active, toggle_available, update_product
from app.services.promotion_service import create_promotion, delete_promotion, list_admin_promotions, update_promotion


router = APIRouter(prefix="/admin", tags=["Admin"], dependencies=[Depends(require_admin)])


@router.get("/products", response_model=list[ProductResponse])
def admin_products(db: Session = Depends(get_db)):
    return list_admin_products(db)


@router.post("/products", response_model=ProductResponse, status_code=201)
def admin_create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, payload)


@router.put("/products/{product_id}", response_model=ProductResponse)
def admin_update_product(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    return update_product(db, product_id, payload)


@router.delete("/products/{product_id}", status_code=204)
def admin_delete_product(product_id: int, db: Session = Depends(get_db)):
    delete_product(db, product_id)


@router.patch("/products/{product_id}/toggle-active", response_model=ProductResponse)
def admin_toggle_active(product_id: int, db: Session = Depends(get_db)):
    return toggle_active(db, product_id)


@router.patch("/products/{product_id}/toggle-available", response_model=ProductResponse)
def admin_toggle_available(product_id: int, db: Session = Depends(get_db)):
    return toggle_available(db, product_id)


@router.get("/categories", response_model=list[CategoryResponse])
def admin_categories(db: Session = Depends(get_db)):
    return list_categories(db)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def admin_create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, payload)


@router.put("/categories/{category_id}", response_model=CategoryResponse)
def admin_update_category(category_id: int, payload: CategoryUpdate, db: Session = Depends(get_db)):
    return update_category(db, category_id, payload)


@router.delete("/categories/{category_id}", status_code=204)
def admin_delete_category(category_id: int, db: Session = Depends(get_db)):
    delete_category(db, category_id)


@router.get("/combos", response_model=list[ComboResponse])
def admin_combos(db: Session = Depends(get_db)):
    return list_admin_combos(db)


@router.post("/combos", response_model=ComboResponse, status_code=201)
def admin_create_combo(payload: ComboCreate, db: Session = Depends(get_db)):
    return create_combo(db, payload)


@router.put("/combos/{combo_id}", response_model=ComboResponse)
def admin_update_combo(combo_id: int, payload: ComboUpdate, db: Session = Depends(get_db)):
    return update_combo(db, combo_id, payload)


@router.delete("/combos/{combo_id}", status_code=204)
def admin_delete_combo(combo_id: int, db: Session = Depends(get_db)):
    delete_combo(db, combo_id)


@router.patch("/combos/{combo_id}/toggle-active", response_model=ComboResponse)
def admin_toggle_combo_active(combo_id: int, db: Session = Depends(get_db)):
    return toggle_combo_active(db, combo_id)


@router.patch("/combos/{combo_id}/toggle-available", response_model=ComboResponse)
def admin_toggle_combo_available(combo_id: int, db: Session = Depends(get_db)):
    return toggle_combo_available(db, combo_id)


@router.get("/promotions", response_model=list[PromotionResponse])
def admin_promotions(db: Session = Depends(get_db)):
    return list_admin_promotions(db)


@router.post("/promotions", response_model=PromotionResponse, status_code=201)
def admin_create_promotion(payload: PromotionCreate, db: Session = Depends(get_db)):
    return create_promotion(db, payload)


@router.put("/promotions/{promotion_id}", response_model=PromotionResponse)
def admin_update_promotion(promotion_id: int, payload: PromotionUpdate, db: Session = Depends(get_db)):
    return update_promotion(db, promotion_id, payload)


@router.delete("/promotions/{promotion_id}", status_code=204)
def admin_delete_promotion(promotion_id: int, db: Session = Depends(get_db)):
    delete_promotion(db, promotion_id)
