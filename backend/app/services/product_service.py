from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.category_model import Category
from app.models.product_model import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate


def _validate_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Categoria inválida.")
    return category


def list_public_products(db: Session) -> list[Product]:
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.is_active.is_(True))
        .order_by(Product.created_at.desc())
        .all()
    )


def list_admin_products(db: Session) -> list[Product]:
    return db.query(Product).options(joinedload(Product.category)).order_by(Product.created_at.desc()).all()


def get_product(db: Session, product_id: int, public_only: bool = False) -> Product:
    query = db.query(Product).options(joinedload(Product.category)).filter(Product.id == product_id)
    if public_only:
        query = query.filter(Product.is_active.is_(True))
    product = query.first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")
    return product


def create_product(db: Session, payload: ProductCreate) -> Product:
    _validate_category(db, payload.category_id)
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return get_product(db, product.id)


def update_product(db: Session, product_id: int, payload: ProductUpdate) -> Product:
    product = get_product(db, product_id)
    data = payload.model_dump(exclude_unset=True)
    if "category_id" in data:
        _validate_category(db, data["category_id"])
    for field, value in data.items():
        setattr(product, field, value)
    db.commit()
    db.refresh(product)
    return get_product(db, product.id)


def delete_product(db: Session, product_id: int) -> None:
    product = get_product(db, product_id)
    db.delete(product)
    db.commit()


def toggle_active(db: Session, product_id: int) -> Product:
    product = get_product(db, product_id)
    product.is_active = not product.is_active
    db.commit()
    db.refresh(product)
    return get_product(db, product.id)


def toggle_available(db: Session, product_id: int) -> Product:
    product = get_product(db, product_id)
    product.is_available = not product.is_available
    db.commit()
    db.refresh(product)
    return get_product(db, product.id)
